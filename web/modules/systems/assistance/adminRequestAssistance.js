var app = angular.module('mainApp');

app.controller('AdminRequestAssistanceCtrl', function($scope, $filter,$timeout, Assistance, Users, Profiles, Session, Notifications, Utils) {

    // requests = [{id:'',license:'',user:{name:'',lastname:'',dni:''},date:''}]
    $scope.model = {
        requests : [],
        justifications: []
    }

    $scope.today;

    $scope.initializeToday = function() {
      $scope.today =  new Date();
      $scope.today.setHours(0);
      $scope.today.setMinutes(0);
      $scope.today.setSeconds(0);
      $scope.today.setMilliseconds(0);
    }


    // ------------ ORDENACION ///////////////////

    $scope.order = function(predicate, reverse) {
      $scope.model.requestsFilters = $filter('orderBy')($scope.model.requestsFilters, predicate, reverse);
    };

    // ------------- FILTRO //////////////////////
    $scope.filter = function() {
      expr = ($scope.filterSelected == null)?'':$scope.filterSelected;
      $scope.model.requestsFilters = $scope.model.requests;
      $scope.model.requestsFilters = $filter('filter')($scope.model.requestsFilters,expr,status);
      $scope.order(['date','user.lastname','user.name'],false);
    }



    $scope.addRequest = function(data) {
        //data: {id:"1",user_id:"1",justification_id: "1", begin: '2015-05-13 00:00:00', end: '2015-05-13 00:00:00', state: "Desaprobada" },
        var r = data;

        r.date = new Date(data.begin);
        r.dateStr = Utils.formatDate(r.date);
        r.user = null;

        if(r.displayHours){
          var begin = new Date(r.begin);
          var end = new Date(r.end);
          r.time = Utils.getDifferenceTimeFromDates(begin, end);
          r.start = Utils.formatTime(begin);
          r.end = Utils.formatTime(end);
        }

        r.disabled = false;

        Users.findUser(data.user_id,
            function(response) {
              r.user = response;
              r.license = Utils.getJustification(r.justification_id);
              $scope.model.requests.push(r);
            },
            function(error) {
            }
        );
    }

    $scope.loadRequests = function() {
        Assistance.getJustificationRequestsToManage(['PENDING','APPROVED'],"TREE",
            function(response) {
              $scope.model.requests = [];
              for (var i = 0; i < response.length; i++) {
                  var show = $scope.today <= new Date(response[i].begin);
                  if (show) {

                    var r = response[i];
                    r.displayHours = false;
                    id = r.justification_id;
                    if (id == 'fa64fdbd-31b0-42ab-af83-818b3cbecf46') {
                      // boleta de salida
                      r.displayHours = true;
                    }
                    $scope.addRequest(r);
                  }
              }
              $scope.model.requestsFilters = $scope.model.requests;
              $scope.filter();
              $scope.order(['date','user.lastname','user.name'],false);
            },
            function(error) {
              Notifications.message(error);
            }
        );
    }

    $scope.initialize = function() {
        $scope.disabled = false;
        $scope.filterSelected = 'PENDING';
        $scope.initializeToday();
        var s = Session.getCurrentSession();
        if (!s || !s.user_id) {
            Notifications.message("Error: sesion no definida");
			      $window.location.href = "/#/logout";
        } else {
            $scope.user_id = s.user_id;
            Profiles.checkAccess(Session.getSessionId(),'ADMIN-ASSISTANCE,USER-ASSISTANCE',
      				function(ok) {
      					if (ok == 'granted') {
                  $scope.loadRequests();
      					}
      				},
      				function (error) {
      					Notifications.message(error);
      				}
      			);
        }
    };


    $scope.updateStatus = function(status, request) {
        $scope.disabled = true;
        Assistance.updateJustificationRequestStatus(request.id, status,
            function(ok) {
              $scope.disabled = false;
                /*
                  ya no es necesario
                Notifications.message("El estado fue modificado correctamente");
                $scope.loadRequests();
                */
            },
            function(error) {
              $scope.disabled = false;
            }
        );
    };

    $scope.approveRequest = function(request) {
        $scope.updateStatus("APPROVED",request);
    };

    $scope.refuseRequest = function(request) {
        $scope.updateStatus("REJECTED",request);
    }

    $scope.cancelRequest = function(request) {
        $scope.updateStatus("CANCELED",request);
    }


    $scope.$on('JustificationsRequestsUpdatedEvent', function(event, data) {
      $scope.loadRequests();
    });

    $scope.$on('JustificationStatusChangedEvent', function(event, data) {
      $scope.loadRequests();
    });



    $timeout(function() {
      $scope.initialize();
    }, 0);


})

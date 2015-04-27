var app = angular.module('mainApp');

app.controller('AdminRequestAssistanceCtrl', function($scope, $timeout, Assistance, Users, Profiles, Session, Notifications, Utils) {

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
    }

    $scope.getJustificationName = function(id) {
      for (var i = 0; i < $scope.model.justifications.length; i++) {
        if ($scope.model.justifications[i].id == id) {
          return $scope.model.justifications[i].name;
        }
      }
    }


    $scope.getJustifications = function() {
      Assistance.getJustifications(
        function(justifications) {
          $scope.model.justifications = justifications;
          $scope.loadRequests();
        },
        function(error) {
        }
      );

    }

    $scope.addRequest = function(data) {
        //data: {id:"1",user_id:"1",justification_id: "1", begin: '2015-05-13 00:00:00', end: '2015-05-13 00:00:00', state: "Desaprobada" },
        var d = new Date(data.begin);

        var r = data;
        r.date = d.toLocaleDateString();
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
              r.licence = $scope.getJustificationName(r.justification_id);
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
                  console.log(new Date(response[i].begin));
                  console.log($scope.today);
                  if ($scope.today <= new Date(response[i].begin)) {

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
            },
            function(error) {
              Notifications.message(error);
            }
        );
    }

    $scope.initialize = function() {
        $scope.disabled = false;
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
                  $scope.getJustifications();
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

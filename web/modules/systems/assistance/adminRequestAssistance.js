var app = angular.module('mainApp');

app.controller('AdminRequestAssistanceCtrl', function($scope, $timeout, Assistance, Users, Profiles, Session, Notifications) {

    // requests = [{id:'',license:'',user:{name:'',lastname:'',dni:''},date:''}]
    $scope.model = {
        requests : [],
        justifications: []
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
        Assistance.getJustificationRequestsToManage(['PENDING'],"TREE",
            function(response) {
              $scope.model.requests = [];
              for (var i = 0; i < response.length; i++) {
                  $scope.addRequest(response[i]);
              }
            },
            function(error) {
              Notifications.message(error);
            }
        );
    }

    $scope.initialize = function() {
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


    $scope.updateStatus = function(status, request_id) {
        Assistance.updateJustificationRequestStatus(request_id, status,
            function(ok) {
                /*
                  ya no es necesario
                Notifications.message("El estado fue modificado correctamente");
                $scope.loadRequests();
                */
            },
            function(error) {

            }
        );
    };

    $scope.approveRequest = function(request) {
        $scope.updateStatus("APPROVED",request.id);
    };

    $scope.refuseRequest = function(request) {
        $scope.updateStatus("REJECTED",request.id);
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

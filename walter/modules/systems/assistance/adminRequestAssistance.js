var app = angular.module('mainApp');

app.controller('AdminRequestAssistanceCtrl', function($scope, $timeout, Assistance, Users, Profiles, Session, Notifications) {

    // requests = [{id:'',license:'',user:{name:'',lastname:'',dni:''},date:''}]
    $scope.model = {
        requests : [],
        requestMap: new Map()
    }
    $scope.justifications = new Map();

    $scope.addRequest = function(data) {
        //data: {request_id:"1",user_id:"1",justification_id: "1", begin: '2015-05-13 00:00:00', end: '2015-05-13 00:00:00', state: "Desaprobada" },
        var r = {};
        r.license = $scope.justifications.get(data.justification_id);
        r.date = data.begin;
        r.user = null;
        r.id = data.request_id;

        var reqs = $scope.model.requestMap.get(data.user_id);
        if (reqs == null) {
            reqs = [];
        }
        reqs.push(r);
        $scope.model.requestMap.set(data.user_id,reqs);

        Users.findUser($scope.user_id,
            function(response) {
                var reqs = $scope.model.requestMap.get(response.id);
                for (x in reqs) {
                    var r = reqs[x];
                    if (r.user == null) {
                        r.user = response;
                        $scope.model.requests.push(r);
                    }
                }
                $scope.model.requestMap.set(response.id,[]);
            },
            function(error) {
            }
        );
    }

    $scope.loadRequests = function() {
        $scope.model.requests = [];
        Assistance.getJustificationRequests("PENDING",null,
            function(response) {
                for (x in response) {
                    $scope.addRequest(response[x]);
                }
            },
            function(error) {

            }
        );
    }

    $scope.getJustifications = function() {
        Assistance.getJustifications(
            function(response) {
                $scope.justifications = new Map();
                for (x in response) {
                    var r = response[x];
                    switch(r.name) {
                        case "absent": name = "Ausente con Aviso"; break;
                        case "compensatory": name = "Compensatorio"; break;
                        default: name = r.name; break;
                    }
                    $scope.justifications.set(r.id,name);
                    $scope.loadRequests();
                }
            },
            function(error) {

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
            Profiles.checkAccess(Session.getSessionId(),'ADMIN-ASSISTANCE',
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

    $timeout(function() {
        $scope.initialize();
    }, 0);

    $scope.updateStatus = function(status, request_id) {
        Assistance.updateStatusRequestJustification(request_id, status,
            function(ok) {
                Notifications.message("El estado fue modificado correctamente");
                $scope.loadRequests();
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


})

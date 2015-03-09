var app = angular.module('mainApp');

app.controller('AssistanceCtrl', function($scope, $timeout, Profiles, Session, Users) {

    $scope.user = {};

    $scope.clearUser = function() {
        $scope.user = {id:'',name:'',lastname:'',dni:''};
    }

    $scope.loadUserData = function() {
        var s = Session.getCurrentSession();
        if (s == null) {
            return;
        }

        Profiles.checkAccess(Session.getSessionId(),'ADMIN-ASSISTANCE,USER-ASSISTANCE', function(ok) {
            if (ok == 'granted') {
                console.log("granted");

                var uid = s.user_id;
                Users.findUser(uid,
                    function(user) {
                        $scope.user = user;
                    },
                    function(error) {
                        alert(error);
                        $scope.clearUser();
                    }
                );
            } else {
                console.log("not granted");
                $scope.clearUser();
            }
        },
        function (error) {
            alert(error);
        });
    }

    $timeout(function() {
      $scope.clearUser();
      $scope.loadUserData();
    }, 0);
});

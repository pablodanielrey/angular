
app.controller('IndexCtrl',IndexCtrl);

IndexCtrl.$inject = ['$rootScope','$scope','$wamp','$window', 'Notifications', 'Login'];

function IndexCtrl($rootScope, $scope, $wamp, $window, Notifications, Login) {

    $scope.model = {
      hideMenu: false
    };

    $scope.hideMenu = function() {
      return $scope.model.hideMenu;
    }

    $scope.initialize = initialize;
    function initialize() {
      /*  if (!Login.isLogged()) {
          $window.location.href = "/systems/login/index.html";
        }*/

        /*Login.validateSession(
          function(v) {
            if (!v) {
              $window.location.href = "/systems/login/index.html";
            }
          },
          function(err) {
            Notifications.message(err);
        })*/
      }

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });

};

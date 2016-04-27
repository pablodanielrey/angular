
app.controller('IndexCtrl',IndexCtrl);

IndexCtrl.$inject = ['$rootScope','$scope', '$window', 'Notifications', 'Login'];

function IndexCtrl($rootScope, $scope, $window, Notifications, Login) {

    $scope.model = {
      hideMenu: false
    };

    $scope.hideMenu = function() {
      return $scope.model.hideMenu;
    }

    $scope.initialize = initialize;

    function initialize() {

      Login.getSessionData()
      .then(function(s) {
        console.log(s);
      }, function(err) {
        $window.location.href = "/systems/login/index.html";
      })
    }

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });

};

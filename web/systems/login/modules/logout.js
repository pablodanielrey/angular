
var app = angular.module('mainApp');

app.controller('LogoutCtrl', function($scope, $window, Session, Login) {

  $scope.logout = function() {

    Login.logout(
      function(ok) {
        Session.destroy();
        $scope.$emit('logoutOk','');
        console.log("logout");
         $window.location.href = "/systems/login/index.html";
      },
      function(error) {
          alert(error);
      });
  };

  $scope.logout();

});

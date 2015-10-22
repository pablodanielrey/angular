
var app = angular.module('mainApp');

app.controller('LogoutCtrl', function($scope, $window, Session, Login) {

  $scope.logout = function() {

    Login.logout(
      function(ok) {
        Session.destroy();
        $scope.$emit('logoutOk','');
         $window.location.href = "/systems/login/indexLogin.html";
      },
      function(error) {
          //alert(error);
      });
  };

  $scope.logout();

});

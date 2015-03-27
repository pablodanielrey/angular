
var app = angular.module('mainApp');

app.controller('LogoutCtrl', function($scope, $location, Session, Credentials) {

  $scope.logout = function() {

    Credentials.logout(
      function(ok) {
        Session.destroy();
        $scope.$emit('logoutOk','');
        $location.path('/');
      },
      function(error) {
          alert(error);
      });
  };

  $scope.logout();

});


(function() {
  var app = angular.module('library');

  app.controller('LoginCtrl', ["$rootScope", '$scope', "Login", function ($rootScope, $scope, Login) {

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });

    $scope.initialize = function() {
      $scope.message = 'pantalla inicial de login';
      $scope.creds = Login.getCredentials();
    };


  }]);
})();

angular
  .module('mainApp')
  .controller('ResetPasswordCtrl', ResetPasswordCtrl);

ResetPasswordCrt.$inject = ['$rootScope','$scope'];

function ResetPasswordCtrl($rootScope, $scope) {

    $scope.screens = ["pantallaDNI", "pantallaCodigo", "pantallaContrasena", "pantallaFin", "pantallaSinCorreoAlternativo"];
    $scope.errors = ["noExisteDNI", "errorDeCodigo", "errorDeContrasena"];
    $scope.screen = "";
    $scope.dni = "";
    $scope.

    $scope.pantalla1 = function() {
      $scope.screen = $scope.screens[0];
    };

    $scope.pantalla2 = function() {
      $scope.screen = $scope.screens[1];
    };


    $rootScope.loaded = false;
    $scope.loaded = false;

    $rootScope.$on("$wamp.open", function (event, session) {
      $scope.$broadcast('wampOpenEvent', event);
    });

    $rootScope.$on("$wamp.close", function (event, session) {
      $scope.$broadcast('wampCloseEvent',event);
    });

    $scope.$on('$viewContentLoaded', function(event) {
      // nada
    });

};

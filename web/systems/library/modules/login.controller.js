
var app = angular.module('library');

app.controller('LoginCtrl', ["$rootScope", '$scope', "$wamp", function ($rootScope, $scope, $wamp) {

  $scope.message = "desconectado";

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  $scope.initialize = function() {
    $scope.message = 'pantalla inicial de login';
  };

  $scope.getPassword = function() {
    console.log('retornando clave : ');
    console.log($scope.password);
    return $scope.password;
  }

  $scope.$on("$wamp.open", function(event, info) {
    console.log(info.session);
    console.log(info.details);
    $scope.message = 'Conexión abierta';
  });

  $scope.$on("$wamp.close", function(event, info) {
    console.log(info.session);
    console.log(info.details);
    $scope.message = 'Conexión cerrada';
  });


  $scope.$on("$wamp.onchallenge", function (event, info) {
    // info.promise: promise to return to wamp,
    // info.session: wamp session,
    // info.method: auth method,
    // info.extra: extra
    //ie. wamp-cra
    console.log('onChallenge')
    return info.promise.resolve($scope.password);
  });

  $scope.login = function() {
    console.log('login llamando')
    console.log($scope.username);
    console.log($scope.password);

    console.log('seteando autentificación y abriendo conexión')
    $wamp.setAuthId($scope.username);
    $wamp.open();
  };


}]);

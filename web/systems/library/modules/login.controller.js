
var app = angular.module('library');

app.controller('LoginCtrl', ["$rootScope", '$scope', "$wamp", function ($rootScope, $scope, $wamp) {

  /*
    función que no depende de este scope si no que esta en el módulo principal.
    ya que aunque no este cargado la pantalla de logín el wamp reintenta la conexión usando las
    credenciales definidas.
  */
  $rootScope.getPassword = function() {
    console.log('retornando clave : ');
    console.log($rootScope.credentials.password);
    return $rootScope.credentials.password;
  }

  $rootScope.$on("$wamp.onchallenge", function (event, info) {
    // info.promise: promise to return to wamp,
    // info.session: wamp session,
    // info.method: auth method,
    // info.extra: extra
    //ie. wamp-cra
    console.log('onChallenge')
    return info.promise.resolve($rootScope.getPassword());
  });



  $scope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  $scope.initialize = function() {
    $scope.message = 'pantalla inicial de login';
    $scope.open = $wamp.connection.isOpen;
    if ($scope.open) {
      $scope.username = $rootScope.credentials.username;
      $scope.password = $rootScope.credentials.password;
    }
  };


  $scope.$on("$wamp.open", function(event, info) {
    console.log(info.session);
    console.log(info.details);
    $scope.message = 'Conexión abierta';
    $scope.open = true;
  });

  $scope.$on("$wamp.close", function(event, info) {
    console.log(info.session);
    console.log(info.details);
    $scope.message = 'Conexión cerrada';
  });

  $scope.close = function() {
    $wamp.close();
  }

  $scope.login = function() {
    console.log('login llamando')
    console.log($scope.username);
    console.log($scope.password);

    console.log('seteando autentificación y abriendo conexión');
    $rootScope.credentials =  {
      username: $scope.username,
      password: $scope.password
    };

    $wamp.setAuthId($rootScope.credentials.username);
    $wamp.open();
  };


}]);

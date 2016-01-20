


/**
 * controlador principal. Funciones principales:
 * 		Verificar la conexión y autentificación de usuarios.
 * 		Recibir eventos del socket y transferirlo a los controladores secundarios
 */
app.controller('IndexCtrl', function ($rootScope,$scope,$location,$window,$wamp,Login) {
  $scope.initialize = initialize;

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  function initialize() {
    if (!Login.isLogged()) {
      $window.location.href = "/systems/login/index.html";
    }

    Login.validateSession(
      function(v) {
        if (!v) {
          $window.location.href = "/systems/login/index.html";
        }
      },
      function(err) {
        Notifications.message(err);
    })
  }

});

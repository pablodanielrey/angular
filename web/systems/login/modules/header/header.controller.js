angular
  .module('login')
  .controller('HeaderCtrl', HeaderCtrl)

HeaderCtrl.$inject = ['$rootScope', '$scope'];

function HeaderCtrl($rootScope, $scope, $window) {

  $rootScope.$on("$wamp.open", function (event, session) {
    // TODO: aca debe actualizar el ícono para que diga que esta conectado
  });

  $rootScope.$on("$wamp.close", function (event, session) {
    // TODO: aca debe actualizar el ícono para que diga que esta desconectado
  });

  $scope.$on('$viewContentLoaded', function(event) {
    // si hay que obtener datos para cargar en el header en este método es el momento de hacerlo.
  });

}


// defino el módulo principal.
var app = angular.module('mainApp',['ngRoute']);


// agrego el controlador principal.

app.controller('IndexCtrl', function ($rootScope, $location, Session) {

    // mensajes que vienen del socket. solo me interesan los eventos, las respuestas son procesadas por otro lado.
    $rootScope.$on('onSocketMessage', function(event, data) {
      var response = JSON.parse(data);

      // analizo el tipo de evento desde el server.
      if (response.type == undefined) {
        return;
      }

      if (response.type == 'Exception') {
        $rootScope.processGeneralExceptions(response);
        return;
      }

      $rootScope.$broadcast(response.type,response.data);
    });


    $rootScope.processGeneralExceptions = function(e) {
      if (e.name == 'SessionNotFound') {
        // debo desloguear al usuario ya que no se encontro en el server remoto.
        $location.path('/logout');
        return;
      }
    }

    // errores de applicacion
    $rootScope.$on('onAppError', function(event, data) {
      alert("error de aplicacion " + data);
    });

    // cambia la url de la pagina en base al evento.
    $rootScope.$on('routeEvent', function(event, data) {
      $location.path(data);
    });


/*
    $rootScope.$on('$routeChangeStart', function(event, next, current) {
      if (!Session.isLogged()) {
//        event.preventDefault();
        $location.path('/login');
      }
    });
*/


/*
    // chequeo que cuando se cambia la navegación se este logueado. si no que vaya a la pantalla de login.
    $rootScope.$on('$afterRouteChange', function(current, previous) {
      alert("afterroutechange");
      if (!Session.isLogged()) {
        $location.path('/login');
      }
    });

    // chequeo que cuando se cambia la navegación se este logueado. si no que vaya a la pantalla de login.
    $rootScope.$on('$afterLocationChange', function(current, previous) {
      alert("afterlocationchange");
      if (!Session.isLogged()) {
        $location.path('/login');
      }
    });
*/


    // la vista por defecto.
//    $location.path('/main');

});


// defino el módulo principal.
var app = angular.module('mainApp',['ngRoute']);


// agrego el controlador principal.

app.controller('IndexCtrl', function ($rootScope, $location, Session, Cache) {

    // mensajes que vienen del socket. solo me interesan los eventos, las respuestas son procesadas por otro lado.
    $rootScope.$on('onSocketMessage', function(event, data) {
      var response = JSON.parse(data);

      // por las dudas si esta cacheado algo lo remuevo, si es una respuesta.
      if ((response.type != undefined) && (/.*Event$/.test(response.type))) {
        Cache.removeItem(response.data);
      }

      // tiene que tener tipo si o si.
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
        // no se encontro la session en el server asi que la destruyo y vuelvo a la pantlla principal.
        Session.destroy();
        $location.path('/main');
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

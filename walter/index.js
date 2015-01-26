
// defino el módulo principal.
var app = angular.module('mainApp',['ngRoute']);


// agrego el controlador principal.

app.controller('IndexCtrl', function ($rootScope, $location, Session, Cache, WebSocket) {


    // mensajes que vienen del socket. solo me interesan los eventos, las respuestas son procesadas por otro lado.
    $rootScope.$on('onSocketMessage', function(event, data) {
      var response = JSON.parse(data);

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
        alert("no se encontro la sesion en el servidor, debe loguearse nuevamente");
        Session.destroy();
        $location.reload();
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


    WebSocket.registerHandlers();


    // la vista por defecto.
//    $location.path('/main');

});

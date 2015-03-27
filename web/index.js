
// defino el módulo principal.
var app = angular.module('mainApp',['ngRoute', 'pickadate']);


/**
 * controlador principal. Funciones principales:
 * 		Verificar la conexión y autentificación de usuarios.
 * 		Recibir eventos del socket y transferirlo a los controladores secundarios
 */
app.controller('IndexCtrl', function ($rootScope, $scope, $location, $timeout, $window, Session, Cache, WebSocket) {

    $rootScope.isLogged = function() {
      return Session.isLogged();
    }

    $rootScope.isConnected = function() {
      return WebSocket.isConnected();
    }


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

      console.log(response.type);
      $rootScope.$broadcast(response.type,response.data);
    });

    $rootScope.processGeneralExceptions = function(e) {

      if (e.name == 'SessionNotFound') {
        // no se encontro la session en el server asi que la destruyo y vuelvo a la pantlla principal.
        alert("no se encontro la sesion en el servidor, debe loguearse nuevamente");
        Session.destroy();
        $window.location.reload();
        return;
      } else if(e.name == "NotImplemented"){
      	console.log("Mensaje no implementado en el servidor");
		$location.path("/main");
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


    $timeout(function() {
      WebSocket.registerHandlers();
    }, 0);


    console.log('index');
    $rootScope.$broadcast('LoginEvent');

    // la vista por defecto.
//    $location.path('/main');

});

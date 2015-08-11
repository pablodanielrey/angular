


/**
 * controlador principal. Funciones principales:
 * 		Verificar la conexión y autentificación de usuarios.
 * 		Recibir eventos del socket y transferirlo a los controladores secundarios
 */
app.controller('IndexCtrl', function ($rootScope, $scope, $location, $timeout, $window, Session, Cache, WebSocket) {

    $scope.global = {
      sessionUserId: null
    };

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
        Session.destroy();
        $window.location.href = "/systems/login/indexLogin.html";
        return;
      }

      if(e.name == "NotImplemented"){
      	console.log("Mensaje no implementado en el servidor");
		    $location.path("/main");
      }

    }


    $timeout(function() {
      WebSocket.registerHandlers();
       if(!Session.isLogged()) {
        $window.location.href = "/systems/login/indexLogin.html";
      }
    }, 0);


});

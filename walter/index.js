
// defino el módulo principal.
var app = angular.module('mainApp',['ngRoute','ngCookies']);


// agrego el controlador principal.

app.controller('IndexCtrl',

  function ($rootScope, $location, Session) {

    // mensajes que vienen del socket.
    $rootScope.$on('onMessageSocket', function(event, data) {
      var response = JSON.parse(data);

      if(response.id == undefined) {
        alert('la respuesta no tiene id : ' + data);
        return;
      }

      $rootScope.$broadcast('onMessage', response);
    });


    // errores de applicacion
    $rootScope.$on('onAppError', function(event, data) {
      alert("error de aplicacion " + data);
    });

    // cambia la url de la pagina en base al evento.
    $rootScope.$on('routeEvent', function(event, data) {
      $location.path(data);
    });

  }

);

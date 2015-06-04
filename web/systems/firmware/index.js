var app = angular.module('mainApp',['ngRoute']);

app.controller('IndexCtrl', function($rootScope,$location,$timeout,WebSocket) {

  // mensajes que vienen del socket. solo me interesan los eventos, las respuestas son procesadas por otro lado.
  $rootScope.$on('onSocketMessage', function(event, data) {
    var response = JSON.parse(data);
    console.log(response);

    // tiene que tener tipo si o si.
    if (response.type == undefined) {
      return;
    }
    console.log(response.type);
    $rootScope.$broadcast(response.type,response.data);
  });


  // cambia la url de la pagina en base al evento.
  $rootScope.$on('routeEvent', function(event, data) {
    $location.path(data);
  });


  $timeout(function() {
    WebSocket.registerHandlers();
  },0);


});

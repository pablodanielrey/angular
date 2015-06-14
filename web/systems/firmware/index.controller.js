angular
    .module('mainApp')
    .controller('IndexController',IndexController);

IndexController.$inject = ['$rootScope','$location','$timeout','WebSocket'];

function IndexController($rootScope,$location,$timeout,WebSocket) {

  // mensajes que vienen del socket. solo me interesan los eventos, las respuestas son procesadas por otro lado.
  $rootScope.$on('onSocketMessage', function(event, data) {

    var response = JSON.parse(data);

    // tiene que tener tipo si o si.
    if (response.type == undefined) {
      return;
    }
    $rootScope.$broadcast(response.type,response.data);
  });


  // cambia la url de la pagina en base al evento.
  $rootScope.$on('routeEvent', function(event, data) {
    $location.path(data);
  });


  $timeout(function() {
    WebSocket.registerHandlers();
  },0);


}

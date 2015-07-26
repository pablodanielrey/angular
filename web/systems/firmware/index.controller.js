angular
    .module('mainApp',['ngRoute','vxWamp'])
    .controller('IndexController',IndexController)
    .config(function($wampProvider) {

      var conn = {
        url: config_firmware.url,
        realm: config_firmware.realm
      };
      console.log(conn);
      $wampProvider.init(conn);
    });
    /*
    .run(function($wamp) {
      $wamp.open();
    });
    */

IndexController.$inject = ['$rootScope','$scope','$location','$timeout','$wamp'];

function IndexController($rootScope,$scope,$location,$timeout,$wamp) {

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


  /*
  $timeout(function() {
    WebSocket.registerHandlers();
  },0);
*/

  $scope.$on('$viewContentLoaded', function(event) {
    $wamp.open();
  });


}

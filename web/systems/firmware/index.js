var app = angular.module('mainApp',['ngRoute']);

app.controller('IndexCtrl', function($rootScope) {

  // mensajes que vienen del socket. solo me interesan los eventos, las respuestas son procesadas por otro lado.
  $rootScope.$on('onSocketMessage', function(event, data) {
    var response = JSON.parse(data);

    // tiene que tener tipo si o si.
    if (response.type == undefined) {
      return;
    }
    console.log(response.type);
    $rootScope.$broadcast(response.type,response.data);
  });


});

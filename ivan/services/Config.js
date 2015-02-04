
var app = angular.module('mainApp');

app.service('Config', function($http) {

  this.websocket = config;

  instance = this;
/*
no la voy a usar por ahora


  this.initialize = function() {
    $http.get('config.json').
    success(function(data, status, headers, config) {
      instance.websocket = data;
      alert(instance.websocket);
    }).
    error(function(data, status, headers, config) {
      alert('el sistema no pudo obtener la configuración, algunas funciones no estarán disponibles');
    })
  }
*/

  this.getWebsocketConnectionUrl = function() {
    return this.websocket.proto + '://' + this.websocket.host + ':' + this.websocket.port;
  }

  this.getServerUrl = function() {
    return document.URL;
  }

//  this.initialize();

});


var app = angular.module('mainApp');

app.service('Config', function($http) {

  this.websocket = {
    proto: 'ws',
    host: '192.168.0.100',
    port: '8001'
  }

  instance = this;

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


  this.getWebsocketConnectionUrl = function() {
    return this.websocket.proto + '://' + this.websocket.host + ':' + this.websocket.port;
  }

  this.getServerUrl = function() {
    return document.URL;
  }

  this.initialize();

});

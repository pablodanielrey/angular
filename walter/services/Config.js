
var app = angular.module('mainApp');

app.service('Config', function() {

  this.websocket = {
    proto: 'ws',
    host: '192.168.0.100',
    port: '8001'
  }

  this.getWebsocketConnectionUrl = function() {
    return this.websocket.proto + '://' + this.websocket.host + ':' + this.websocket.port;
  }

  this.getServerUrl = function() {
    return document.URL;
  }

});

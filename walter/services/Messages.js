
var app = angular.module('mainApp');

app.service('Messages', function($rootScope, WebSocket) {

  this.ids = [];

  this.send = function(msg) {
    WebSocket.send(JSON.stringify(msg));
  }

  this.send = function(msg, callback) {
    this.ids.push({
      id:msg.id,
      callback:callback
    });

    WebSocket.send(JSON.stringify(msg));
  }

  this.receive = function(response) {
    for (var i = 0; i < this.ids.length; i++) {
      if (this.ids[i].id == response.id) {
        this.ids[i].callback(response);
        this.ids.splice(i,1);                   // remuevo el id ya que la respuesta ya se proceso.
        break;
      }
    }
  };


  /////////// parte de eventos que se registra /////////////


  var messages = this;

  /*
    Registro un handler del evento de los websockets asi proceso las respuestas.
  */
  $rootScope.$on('onSocketMessage', function(e,data) {
    var response = JSON.parse(data);
    // solo me interesan las respuestas. (type == undefined && id != undefined)
    if (response.type != undefined || response.id == undefined) {
      return;
    }
    messages.receive(response);
  });

  

});

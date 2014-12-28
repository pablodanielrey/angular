
var app = angular.module('mainApp');

app.factory('Messages', function($rootScope, WebSocket) {

  var factory = {};
  factory.ids = [];

  factory.send = function(msg) {
    WebSocket.send(JSON.stringify(msg));
  }

  factory.send = function(msg, callback) {
    this.ids.push({
      id:msg.id,
      callback:callback
    });

    WebSocket.send(JSON.stringify(msg));
  }

  factory.receive = function(response) {
    for (var i = 0; i < factory.ids.length; i++) {
      if (this.ids[i].id == response.id) {
        this.ids[i].callback(response);
        this.ids.splice(i,1);                   // remuevo el id ya que la respuesta ya se proceso.
        break;
      }
    }
  };


  /*
    Registro un handler del evento de los websockets asi proceso las respuestas.
  */

  $rootScope.$on('onSocketMessage', function(e, data) {

    var response = JSON.parse(data);

    // solo me interesan las respuestas. (type == undefined && id != undefined)
    if (response.type != undefined || response.id == undefined) {
      return;
    }

    factory.receive(response);
  });


  return factory;

});

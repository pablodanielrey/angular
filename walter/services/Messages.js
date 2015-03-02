
var app = angular.module('mainApp');

app.service('Messages', function($rootScope, WebSocket) {

  this.ids = [];

  this.send = function(msg) {
    WebSocket.send(JSON.stringify(msg));
  }

  this.send = function(msg, callback) {
    this.ids.push({
      id:msg.id,
      callback:callback,
      parts:{count:0, parts:0}
    });

    WebSocket.send(JSON.stringify(msg));
  }

  this.receive = function(response) {

    // codigo horrible!!! lo hago para hacer una prueba con los mensajes gigantes.
    if (response.parts != undefined) {
      // proceso el mensaje de cabecera indicando la cantidad de partes.
      for (var i = 0; i < this.ids.length; i++) {
        if (this.ids[i].id == response.id) {
          this.ids[i].parts.count = int(response.parts);
          return;
        }
      }
      return;
    }

    // en caso de ser una parte, etnocnes llamo al callback pero sin removerlo.
    if (response.part_number != undefined) {
      // proceso el mensaje parte y lo guardo
      for (var i = 0; i < this.ids.length; i++) {
        if (this.ids[i].id == response.id) {
          this.ids[i].parts.parts += 1;
          this.ids[i].callback(response);
          if (this.ids[i].parts.parts >= this.ids[i].parts.count) {
            this.ids.splice(i,1);              // ya tengo todas las partes. remuevo el callback.
          }
          break;
        }
      }
      return;
    }


    // proceso el mensaje normalmente y elimino el callback en el caso de existir.
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


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
      parts:{count:0, parts:[]}
    });

    WebSocket.send(JSON.stringify(msg));
  }

  this.receive = function(response) {
    /*
    // codigo horrible!!! lo hago para hacer una prueba con los mensajes gigantes.
    if (response.parts != undefined) {

      console.log('recibido un mensaje de cabecera de framming');
      console.log(response.parts + ' partes del mensaje se transmitiran');

      // proceso el mensaje de cabecera indicando la cantidad de partes.
      for (var i = 0; i < this.ids.length; i++) {
        if (this.ids[i].id == response.id) {
          this.ids[i].parts.count = parseInt(response.parts);
          this.ids[i].parts.parts = (new Array(parseInt(response.parts))).map(function(x,i) { return null; }); // un array de la cantidad de partes a null.
          return;
        }
      }
      return;
    }

    // en caso de ser una parte, la guardo para hacer el ensamblado posterior.
    if (response.part_number != undefined) {

      console.log("parte número " + response.part_number);

      // proceso el mensaje parte y lo guardo
      for (var i = 0; i < this.ids.length; i++) {
        if (this.ids[i].id == response.id) {

          // agrego la parte en el indice que va.
          this.ids[i].parts.parts[parseInt(response.part_number)] = window.atob(response.part_data);

          // controlo si ya se tiene todas para llamar al callback.
          var count = 0;
          for (var a = 0; a < this.ids[i].parts.parts.length; a++) {
            if (this.ids[i].parts.parts[a] != null) {
              count = count + 1;
            }
          }
          if (count >= (this.ids[i].parts.count - 1)) {
            // tengo todos. reensamblo y llamo al callback
            var fullmessage = this.ids[i].parts.parts.join("");

            console.log('mensaje completo');
            //console.log(fullmessage);


            //  ACA ES LO QUE TARDA UNA VIDA Y BLOQUEA EL THREAD PRINCIPAL!!! CUANDO SE PASA A JSON

            //var jsonFullMessage = JSON.parse(fullmessage);
            var jsonFullMessage = eval('(' + fullmessage + ')');

            this.ids[i].callback(jsonFullMessage);
            this.ids.splice(i,1);                   // remuevo el id ya que la respuesta ya se proceso.
            return;

          }

          break;
        }
      }
      return;
    }
    */

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

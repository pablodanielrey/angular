angular
  .module('mainApp')
  .service('MyFirstSystem',MyFirstSystem);

Designation.inject = ["$wamp"]


function MyFirstSystem($wamp) {

  /**
    Servicio de llamada a los métodos del servidor.
    todos los métodos de los servicios retornan Promise   
  */

  //***** obtener mensaje *****
  this.getMessage = function() { 
    return $wamp.call('myFirstSystem.getMessage', []); 
  };
  
  
  //***** acceso al servidor de ejemplo con parametros. retorna myfirstentity *****
  this.helloWord = function(param1, param2) { 
    return $wamp.call('myFirstSystem.helloWord', [param1, param2]); 
  };
  
}

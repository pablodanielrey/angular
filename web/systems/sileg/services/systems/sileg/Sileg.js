angular
  .module('mainApp')
  .service('Sileg',Sileg);

Sileg.inject = ['$rootScope','$wamp']



function Sileg($rootScope, $wamp) {

  //***** obtener usuarios con una designacion activa a una catedra *****
  this.getUsers = function() { return $wamp.call('sileg.getUsers'); }
  
  //***** obtener catedras con una designacion activa a una catedra *****
  this.getCathedras = function() { return $wamp.call('sileg.getCathedras'); }
  
  //***** obtener datos completos de una designacion *****
  this.getDesignationFull = function(designationId) { return $wamp.call("sileg.getDesignationFull", [designationId]); }
  
  //***** obtener datos de un usuario de un determinado usuario agrupadas por position *****
  this.getEconoPageDataUser = function(userId) { return $wamp.call('sileg.getEconoPageDataUser', [userId]); }
  
  //***** obtener datos de un usuario de un determinado usuario agrupadas por position *****
  this.getEconoPageDataPlace = function(placeId) { return $wamp.call('sileg.getEconoPageDataPlace', [placeId]); }

}

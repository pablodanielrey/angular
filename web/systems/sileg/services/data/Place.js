angular
  .module('mainApp')
  .service('Place',Place);

Place.inject = ['$rootScope','$wamp']

function Place($rootScope, $wamp) {

  //***** obtener usuarios con una designacion activa a una catedra *****
  this.findById = function(ids) { return $wamp.call('sileg.findPlacesByIds', [ids]); }
  
  //***** obtener usuarios con una designacion activa a una catedra *****
  this.findAll = function() { return $wamp.call('sileg.findPlacesAll'); }  
  
  //***** obtener usuarios con una designacion activa a una catedra *****
  this.findByDescription = function(search) { return $wamp.call('sileg.findPlace', [search]); }
 
}

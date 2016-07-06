angular
  .module('mainApp')
  .service('Designation',Designation);

Designation.inject = ['$rootScope','$wamp']

function Designation($rootScope, $wamp) {

  //***** obtener usuarios con una designacion activa a una catedra *****
  this.findById = function(ids) { return $wamp.call('sileg.findDesignationsByIds', [ids]); }
 
}

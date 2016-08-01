angular
  .module('mainApp')
  .service('Position',Position);

Place.inject = ['$rootScope','$wamp']

function Position($rootScope, $wamp) {

  this.findById = function(ids) { return $wamp.call('sileg.findPositionsByIds', [ids]); }
  
  this.findAll = function() { return $wamp.call('sileg.findPositionsAll') };
}

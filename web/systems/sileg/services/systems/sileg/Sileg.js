angular
  .module('mainApp')
  .service('Sileg',Sileg);

Sileg.inject = ['$rootScope','$wamp']

function Sileg($rootScope, $wamp) {

  //***** get place by id *****
  this.getPlaceById = function(id) {
    return $wamp.call('sileg.getPlaceById',[filters]);
  }

}

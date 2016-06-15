angular
  .module('mainApp')
  .service('Sileg',Sileg);

Sileg.inject = ['$rootScope','$wamp','Session']

function Sileg($rootScope, $wamp, Session) {

  //***** get place by id *****
  this.getPlaceById = function(id) {
    return $wamp.call('sileg.getPlaceById',[filters]);
  }

}

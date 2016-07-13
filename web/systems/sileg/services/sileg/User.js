angular
  .module('mainApp')
  .service('User',User);

User.inject = ['$rootScope','$wamp']

function User($rootScope, $wamp) {

  this.findById = function(ids) { return $wamp.call('sileg.findUsersByIds', [ids]); }
 
}

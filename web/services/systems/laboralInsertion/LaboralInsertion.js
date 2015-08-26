
angular
  .module('mainApp')
  .service('LaboralInsertion',LaboralInsertion);

LaboralInsertion.inject = ['$rootScope','$wamp','Session']

function LaboralInsertion($rootScope,$wamp,Session) {

}

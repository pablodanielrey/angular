angular
  .module('mainApp')
  .service('Office',Office);

Office.inject = ['$rootScope','$wamp'];

function Office($rootScope, $wamp) {

  this.getOffices = function(callbackOk,callbackError) {
    $wamp.call('offices.offices.getOffices', [])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError(err);
    });
  }

  this.getOfficesByUser = function(userId,tree,callbackOk,callbackError) {
    $wamp.call('offices.offices.getOfficesByUser', [userId,tree])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError(err);
    });
  }
}

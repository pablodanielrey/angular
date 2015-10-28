var app = angular.module('mainApp');

app.service('Positions', ['Utils','Session','$wmap',

	function(Utils, Session, $wamp) {

    this.getPosition = function(userId, callbackOk, callbackError){
      var sid = Session.getSessionId();
      $wamp.call('positions.getPosition', [sid, userId])
        .then(function(res) {
          if (res != null) {
            callbackOk(res);
          } else {
            callbackError('Error');
          }
        },function(err) {
          callbackError(err);
        });
    };

    /**
     * Actualizar cargo del usuario
     * @param {userId} userId
     * @param {justificationId} justificationId
     * @param {stock} stock
     */
    this.updatePosition = function(userId, position, callbackOk,callbackError) {
      var sid = Session.getSessionId();
      $wamp.call('positions.updatePosition', [sid, userId, position])
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
]);

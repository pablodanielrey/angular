angular
  .module('mainApp')
  .service('Firmware',Firmware);

Firmware.inject = ['$rootScope','$wamp'];

function Firmware($rootScope, $wamp) {


    /*
    this.enroll = function(sid, dni, callbackOk, callbackError) {
      var msg = {
        id: Utils.getId(),
        action: 'enroll',
        sid: sid,
        request: {
          dni: dni
        }
      }

      Messages.send(msg,
        function(data) {
          if (typeof data.error === 'undefined') {
              callbackOk(data);
          } else {
            callbackError(data.error)
          }
      });
    }

    this.login = function(code, password, callbackOk, callbackError) {
      var msg = {
        id: Utils.getId(),
        action: 'login',
        request: {
          dni: code,
          password: password
        }
      }

      Messages.send(msg,
        function(data) {
          if (typeof data.error === 'undefined') {
              callbackOk(data);
          } else {
            callbackError(data.error)
          }
      });
    }
    */

    this.enroll = function(dni, callbackOk, callbackError) {
      $wamp.call('assistance.firmware.enroll', [dni])
      .then(function() {
          callbackOk();
        }
      ),function(err) {
        callbackError(err);
      };
    }


    this.login = function(dni, password, callbackOk, callbackError) {
      $wamp.call('assistance.firmware.login', [dni,password])
        .then(function(res) {
          console.log(res);
          callbackOk(res);
        }
        ),function(err) {
          console.log(err);
          callbackError(err);
        };
    }


    this.onEnrollEvents = function(needFingerEventHandler,msgEventHandler,errorEventHandler,fatalErrorEventHandler) {
      $wamp.subscribe('assistance.firmware.enroll_need_finger',needFingerEventHandler);
      $wamp.subscribe('assistance.firmware.enroll_show_message',msgEventHandler);
      $wamp.subscribe('assistance.firmware.enroll_error',errorEventHandler);
      $wamp.subscribe('assistance.firmware.enroll_fatal_error',fatalErrorEventHandler);
    }


    this.onIdentified = function(eventManager) {
      $wamp.subscribe('assistance.firmware.identify',eventManager);
    }

};

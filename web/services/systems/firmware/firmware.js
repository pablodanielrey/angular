var app = angular.module('mainApp');

app.service('Firmware', ['Utils','Messages','Session','$rootScope',

  function(Utils,Messages,Session,$rootScope) {

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


  }
]);

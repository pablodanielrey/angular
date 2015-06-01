var app = angular.module('mainApp');

app.service('Firmware', ['Utils','Messages','Session',

  function(Utils,Message,Session) {

    this.enroll = function(dni, callbackOk, callbackError) {
      var msg = {
        id: Utils.getId(),
        action: 'enroll',
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

    this.sendCode = function(code, password, callbackOk, callbackError) {
      callbackOk('admin');
    }


  }
]);

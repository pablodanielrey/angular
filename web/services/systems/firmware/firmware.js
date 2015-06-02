var app = angular.module('mainApp');

app.service('Firmware', ['Utils','Messages','Session','$rootScope',

  function(Utils,Message,Session,$rootScope) {

    this.enroll = function(dni, callbackOk, callbackError) {
      var msg = {
        id: Utils.getId(),
        action: 'enroll',
        request: {
          dni: dni
        }
      }
      /*
      Messages.send(msg,
        function(data) {
          if (typeof data.error === 'undefined') {
              callbackOk(data);
          } else {
            callbackError(data.error)
          }
      });
      */

      $rootScope.$broadcast('MsgEvent',null);
    }

    this.sendCode = function(code, password, callbackOk, callbackError) {
      callbackOk('admin');
      var data = {};
      data.user = {name:'Emanuel',lastname:'Pais',dni:code};
      $rootScope.$broadcast('identifiedEvent',data);
    }


  }
]);

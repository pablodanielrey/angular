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

    this.identify = function(code, password, callbackOk, callbackError) {
      callbackOk('admin');
      var data = {};
      data.user = {name:'Emanuel',lastname:'Pais',dni:code};
      data.profile = 'admin';
      data.date = new Date();
      $rootScope.$broadcast('identifiedEvent',data);
    }


  }
]);

angular
  .module('login')
  .service('Login', Login);

Login.inject = ['$rootScope', '$wampPublic', '$wampCore', '$q'];

function Login($rootScope, $wampPublic, $wampCore, $q) {

  this.getPublicData = function(username) {
    return $wampPublic.call('login.get_public_data', [username]);
  }

  this.login = function(username, password) {

    if ($wampCore.connection != undefined && $wampCore.connection != null && $wampCore.connection.isOpen) {
      $wampCore.close();
    }

    // armo la promesa que tiene en cuenta toda la cadena de eventos posibles.
    var defer = $q.defer();

    // challege del wamp que se autentifica
    $rootScope.$on("$wampCore.onchallenge", function(event, info) {
      // info.promise: promise to return to wamp,
      // info.session: wamp session,
      // info.method: auth method,
      // info.extra: extra
      //ie. wamp-cra
      console.log('retornando clave challenge');
      return info.promise.resolve(password);
    });

    $rootScope.$on("$wampCore.open", function(event, info) {
      console.log(info);
      console.log('obteniendo los sistemas registrados');
      $wampCore.call('login.get_registered_systems').then(
        function(systems) {
          defer.resolve(systems);
        },
        function(err) {
          defer.fail(err);
        });
    });

    $rootScope.$on("$wampCore.error", function(event, info) {
      console.log(info);
      defer.fail(info);
    });

    $wampCore.setAuthId(username);
    $wampCore.open();

    return defer.promise;
  }

  /*
  this.getRegisteredSystems = function() {
    return $wampCore.call('login.get_registered_systems');
  };
  */


  this.hasOneRole = function(roles) {
    return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('system.profile.hasOneRole', [sid, roles])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
  };

};

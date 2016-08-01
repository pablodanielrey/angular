(function() {
  'use strict';

  angular
    .module('login')
    .service('Login', Login);

  Login.$inject = ['$rootScope', '$window', '$q', '$cookies', '$wampPublic', '$wampCore'];

  function Login($rootScope, $window, $q, $cookies, $wampPublic, $wampCore) {
    var service = this;

    service.check = function() {
      var creds = service._getAuthCookie();
      if (creds == null) {
        $window.location.href = '/systems/login/';
        return;
      }

      // debo reconectarme con las nuevas credenciales en caso de no estar conectado
      if (!$wampCore.connection.isOpen) {
        service._login(creds.username, creds.ticket).then(
          function(systems) {
            // nada
          },
          function(err) {
            console.log(err);
            $window.location.href = '/systems/login/';
          }
        );
      }
    }

    service.getCredentials = function() {
      return service._getAuthCookie();
    }

    service.getPublicData = function(username) {
      return $wampPublic.call('login.get_public_data', [username]);
    }

    service.login = function(username, password) {
      if ($wampCore.connection != undefined && $wampCore.connection != null && $wampCore.connection.isOpen) {
        $wampCore.close();
      }
      return service._login(username, password);
    }

    service._login = function(username, password) {

      // armo la promesa que tiene en cuenta toda la cadena de eventos posibles.
      var defer = $q.defer();

      var events = [];

      // challege del wamp que se autentifica
      events.push($rootScope.$on("$wampCore.onchallenge", function(event, info) {
        // info.promise: promise to return to wamp,
        // info.session: wamp session,
        // info.method: auth method,
        // info.extra: extra
        //ie. wamp-cra
        console.log('retornando clave challenge');
        return info.promise.resolve(password);
      }));

      events.push($rootScope.$on("$wampCore.open", function(event, info) {
        console.log(info);

        // seteo la cookie de autentificacion para ese usuario con la info retornada por el autenticador de crossbar.
        service._setAuthCookie(info.details.authextra);

        console.log('obteniendo los sistemas registrados');
        $wampCore.call('login.get_registered_systems').then(
          function(systems) {
            service._deregisterEvents(events);
            defer.resolve(systems);
          },
          function(err) {
            service._deregisterEvents(events);
            defer.reject(err);
          });
      }));

      events.push($rootScope.$on("$wampCore.close", function(event, info) {
        console.log(info);
        service._deregisterEvents(events);
        defer.reject(info);
      }));

      events.push($rootScope.$on("$wampCore.error", function(event, info) {
        console.log(info);
        service._deregisterEvents(events);
        defer.reject(info);
      }));

      $wampCore.setAuthId(username);
      $wampCore.open();

      return defer.promise;
    }

    service.hasOneRole = function(roles) {
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


    /*
      usado para desregistrar los eventos registrados en login() en rootScope para el manejo de wamp.
    */
    service._deregisterEvents = function(events) {
      for (var i = 0; i < events.length; i++) {
        events[i]();
      }
    }

    service._setAuthCookie = function(info) {
      $cookies.putObject('authlogin', info, {path:'/'});
    }

    service._getAuthCookie = function() {
      return $cookies.getObject('authlogin');
    }

    service.connected = 0;

    service._open = function() {
      service.connecetd = service.conected + 1;
      $rootScope.$broadcast('wamp.open');
    }

    service._close = function() {
      service.connected = service.connected - 1;
      if (service.connected <= 0) {
        $rootScope.$broadcast('wamp.close');
      }
    }

    $rootScope.$on('$wampPublic.open', function(event) {
      service._open();
    });

    $rootScope.$on('$wampPublic.close', function(event) {
      service._close();
    });


  };

})();

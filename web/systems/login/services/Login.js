(function() {
  'use strict';

  angular
    .module('login')
    .service('Login', Login);

  Login.$inject = ['$rootScope', '$window', '$q', '$cookies'];

  function wamp(conn) {
    return {
      connection: conn,
      subscribe: function (topic, handler) {
        connection.session.subscribe(topic, handler);
      },
      call: function (procedure, args) {
        return connection.session.call(procedure, args);
      }
    };
  }

  function Login($rootScope, $window, $q, $cookies) {
    var service = this;

    service.username = null;
    service.password = null;
    service.ticket = null;

    service.privateConnection = null;
    service.publicConnection = null;


    service.getPublicTransport = function() {
      return wamp(service.publicConnection);
    }

    service.getPrivateTransport = function() {
      return wamp(service.privateConnection);
    }


    // inicializamos la conexión pública

    var host = '127.0.0.1';
    var options = {
        url: 'ws://' + host + ':80/ws',
        realm: 'public',
        authmethods: ['anonymous']
    };
    service.publicConnection = new autobahn.Connection(options);
    service.publicConnection.onopen = function(session, details) {
      // aca esta abierta la sesión.
      console.log(details);
    }
    service.publicConnection.onclose = function(reason, details) {
      console.log(reason);
      console.log(details);

      if (reason == 'lost') {
        return false;
      }


      /*
      case 'closed':
          // doc
          break;

      case 'lost':
          return true;

      case 'unreachable':
          // doc
          break;

      case 'unsupported':
          // doc
          break;
          */
    }
    service.publicConnection.open();







    /*
      Implementa el chequeo y reconexion para todos los sistemas.
    */
    service.check = function() {
      var creds = service._getAuthCookie();
      if (creds == null) {
        $window.location.href = '/';
        return;
      }

      // debo reconectarme con las nuevas credenciales en caso de no estar conectado
      if (!service.privateConnection.isOpen) {
        service._login(creds.username, creds.ticket).then(
          function(systems) {
            // nada
          },
          function(err) {
            console.log(err);
            $window.location.href = '/';
          }
        );
      }
    }



    service.getCredentials = function() {
      return service._getAuthCookie();
    }

    service.getPublicData = function(username) {
      return service.publicConnection.session.call('login.get_public_data', [username]);
    }


    service.getPrivateConnection = function(username, password) {
      var d = $q.defer();

      var host = '127.0.0.1';
      var options = {
          url: 'ws://' + host + ':80/ws',
          realm: 'core',
          authid: username,
          authmethods: ['ticket'],
          onchallenge: function(session, method, extra) {
            console.log('onchallenge');
            console.log(session);
            console.log(method);
            console.log(extra);
            return password;
          }
      }
      var conn = new autobahn.Connection(options);
      conn.onopen = function(session, details) {
        // aca esta abierta la sesión.
        service._setAuthCookie(details.authextra);
        console.log(details);
        d.resolve(conn);
      }
      conn.onclose = function(reason, details) {
        console.log(reason);
        console.log(details);
        if (reason == 'lost') {
          return false;
        }
        d.reject(new Error(reason));
      }
      conn.open();
      return d
    }


    service.login = function(username, password) {
      var d = $q.defer();
      service.getPrivateConnection(username, password).then(function(conn) {
        service.privateConnection = conn;
        d.resolve('logueado');
      }, function(err) {
        d.reject(err);
      });
      return d.promise;
    }


    /*
    // retorno la cookie de ticket si es que existe para las reconexiones.
    service.autoreconnectauth = function(event, info)  {
      var creds = service._getAuthCookie();
      if (creds == null) {
        $window.location.href = '/';
        return;
      }

      console.log(creds);
      return info.promise.resolve(creds.ticket);
    }
*/

/*
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
        $rootScope.$on("$wampCore.onchallenge", service.autoreconnectauth);

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
*/

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

    service.logout = function() {
      $cookies.remove('authlogin', {path:'/'});
      service.check();
    }

    service._setAuthCookie = function(info) {
      var expires = new Date(info.expires);
      $cookies.putObject('authlogin', info, {path:'/', expires: expires});
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

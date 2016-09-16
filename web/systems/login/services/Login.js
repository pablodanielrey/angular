(function() {
  'use strict';

  angular
    .module('login')
    .factory('wamp', wamp)
    .service('Login', Login);


    function wamp()  {
        var factory  =   {};
        var data  =   {};
        var connection = null;
        data.year = 1975;

        factory.getData =   function ()  {
            return data;
        };

        factory.setData = function(d) {
          data = d;
        };

        factory.init = function(conn) {
          connection = conn;
        };

        factory.subscribe = function(topic, handler) {
          connection.session.subscribe(topic, handler);
        };

        factory.call = function (procedure, args) {
          return connection.session.call(procedure, args);
        };

        factory.calculaEdad = function(edad){
            return 2014 - edad;
        }

        return factory;
    };

    /*
    function wamp() {

      return {
        connection: 'hola',
        Hello: function() {
          return "Hello, World!"
       },
        subscribe: function (topic, handler) {
          connection.session.subscribe(topic, handler);
        },
        call: function (procedure, args) {
          return connection.session.call(procedure, args);
        }
      };

    };
    */

  Login.$inject = ['$rootScope', '$window', '$q', '$cookies', 'wamp'];

  function Login($rootScope, $window, $q, $cookies, wamp) {
    var service = this;

    service.username = null;
    service.password = null;
    service.ticket = null;

    service.privateConnection = null;
    service.publicConnection = null;


    service.getPublicTransport = function() {
      wamp.init(service.publicConnection);
      return wamp;
    }

    service.getPrivateTransport = function() {
      wamp.init(service.privateConnection);
      return wamp;
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
      console.log(details);
    }
    service.publicConnection.onclose = function(reason, details) {
      console.log(reason);
      console.log(details);

      if (reason == 'lost') {
        return false;
      }
    }
    service.publicConnection.open();


    service.check = function() {
      var d = $q.defer();
      var creds = service._getAuthCookie();
      if (creds == null) {
        d.reject("creds == null");
        return d.promise;
      }

      // debo reconectarme con las nuevas credenciales en caso de no estar conectado
      if (service.privateConnection == null || !service.privateConnection.isOpen) {
        service.login(creds.username, creds.ticket).then(
          function(conn) {
            d.resolve(conn);
          },
          function(err) {
            d.reject(err);
          }
        );
      }
      return d.promise;
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
        $rootScope.$broadcast('wamp.open');

        service._setAuthCookie(details.authextra);
        console.log(details);
        d.resolve(conn);
      }
      conn.onclose = function(reason, details) {
        console.log(reason);
        console.log(details);

        $rootScope.$broadcast('wamp.close');

        if (reason == 'lost') {
          return false;
        }
        d.reject(new Error(reason));
      }
      conn.open();
      return d.promise;
    }


    service.login = function(username, password) {
      var d = $q.defer();
      service.getPrivateConnection(username, password).then(function(conn) {
        service.privateConnection = conn;
        d.resolve(conn);
      }, function(err) {
        d.reject(err);
      });
      return d.promise;
    }

    service.getRegisteredSystems = function(conn) {
      return conn.session.call('login.get_registered_systems');
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


    service.logout = function() {
      $cookies.remove('authlogin', {path:'/'});
      service.privateConnection.close();
      $window.location.href = '/';
    }

    service._setAuthCookie = function(info) {
      var expires = new Date(info.expires);
      $cookies.putObject('authlogin', info, {path:'/', expires: expires});
    }

    service._getAuthCookie = function() {
      return $cookies.getObject('authlogin');
    }
  }
})();

(function() {
  'use strict';

  angular
    .module('login')
    .service('Login', Login);

    function wamp(connection)  {
        var factory = {};

        factory.subscribe = function(topic, handler) {
          connection.session.subscribe(topic, handler);
        };

        factory.call = function (procedure, args) {
          return connection.session.call(procedure, args);
        };

        return factory;
    };

  Login.$inject = ['$rootScope', '$window', '$q', '$cookies', '$location'];

  function Login($rootScope, $window, $q, $cookies, $location) {
    var service = this;

    service.username = null;
    service.password = null;
    service.ticket = null;

    service.privateConnection = null;
    service.publicConnection = null;

    service.getPublicTransport = function() {
      if (service.publicConnection == null) {
        return null;
      }
      return wamp(service.publicConnection);
    }

    service.getPrivateTransport = function() {
      if (service.privateConnection == null) {
        return null;
      }
      return wamp(service.privateConnection);
    }


    // inicializamos la conexión pública

    var host = location.host;
    var options = {
        url: 'ws://' + host + '/ws',
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


    /*service.check = function() {
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
            $rootScope.$broadcast('openPrivateConnection');
          },
          function(err) {
            d.reject(err);
          }
        );
      } else {
        d.resolve(service.privateConnection);
      }
      return d.promise;
    }*/


    service.check = function() {
      var creds = service._getAuthCookie();
      if (creds == null) {
        $window.location.href = '/';
        return;
      }

      // debo reconectarme con las nuevas credenciales en caso de no estar conectado
      if (service.privateConnection == null || !service.privateConnection.isOpen) {
        service.login(creds.username, creds.ticket).then(
          function(conn) {
            // 28/10/16 Lo comente porque se dispara en el onOpen del metodo login (Consultar con pa)
            // $rootScope.$broadcast('wamp.open');
          },
          function(err) {
            console.log(err);
            $window.location.href = '/';
          }
        );
      }
    }

    service.redirect = function() {
      var creds = service._getAuthCookie();
      if (creds == null) {
        return;
      }

      // debo reconectarme con las nuevas credenciales en caso de no estar conectado
      if (service.privateConnection == null || !service.privateConnection.isOpen) {
        service.login(creds.username, creds.ticket).then(
          function(conn) {
            service.getRegisteredSystems(conn).then(
            function(systems) {
                console.log(systems);
                for (var i = 0; i < systems['registered'].length; i++) {
                    if ($location.host() == systems['registered'][i].domain) {
                      $window.location.href = systems['registered'][i].relative;
                      return;
                    }
                }
                // si no lo encuentra usa la ultima (deberia ser la de sistema en mantenimiento o algo parecido)
                $window.location.href = systems['default'];
              },
              function(err) {
                 console.error(err);
              });
          },
          function(err) {
          }
        );
      }
    }


    service.getCredentials = function() {
      var creds = service._getAuthCookie();
      if (creds == null) {
        $window.location.href = '/';
        return;
      }
      return creds;
    }

    service.getPublicData = function(username) {
      return service.publicConnection.session.call('login.get_public_data', [username]);
    }


    service.getPrivateConnection = function(username, password) {
      var d = $q.defer();

      var host = location.host;
      var options = {
          url: 'ws://' + host + '/ws',
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
        $rootScope.$apply(function() {
          $rootScope.$broadcast('wamp.open');
          service._setAuthCookie(details.authextra);
          console.log(details);
          d.resolve(conn);
        });
      }
      conn.onclose = function(reason, details) {
        console.log(reason);
        console.log(details);
        $rootScope.$apply(function() {
          $rootScope.$broadcast('wamp.close');
          if (reason == 'lost') {
            return false;
          }
          if (reason == 'closed' && details.reason == 'wamp.error.authentication_failed') {
            $window.location.href = '/';
            return;
          }
          d.reject(new Error(reason));
        });
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

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
  }
})();

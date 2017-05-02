(function() {
  'user strict'
  angular
      .module('tutorias.coordinadores',['ngRoute', 'ui.bootstrap', 'login', 'ngCookies'])
      .run(function(Login, $window) {
        Login.check();
      });
})();

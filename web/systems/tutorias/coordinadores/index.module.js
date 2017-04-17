(function() {
  'user strict'
  angular
      .module('tutorias.coordinadores',['ngRoute', 'ui.bootstrap', 'login','files',])
      .run(function(Login, $window) {
        Login.check();
      });
})();

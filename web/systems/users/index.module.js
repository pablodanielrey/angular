(function() {
  'user strict'
  angular
      .module('users',['ngRoute', 'ui.bootstrap', 'login','files',])
      .run(function(Login, $window) {
        Login.check();
      });
})();

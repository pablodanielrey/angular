(function() {
  'user strict'
  angular
      .module('users.recover',['ngRoute', 'ui.bootstrap', 'login','files',])
      .run(function(Login, $window) {
        Login.check();
      });
})();

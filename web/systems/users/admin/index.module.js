(function() {
  'user strict'
  angular
      .module('users.admin',['ngRoute', 'ui.bootstrap', 'login','files',])
      .run(function(Login, $window) {
        Login.check();
      });
})();

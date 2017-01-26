(function() {
  'user strict'
  angular
      .module('users.profile',['ngRoute', 'ui.bootstrap', 'login','files',])
      .run(function(Login, $window) {
        Login.check();
      });
})();

(function() {
  'user strict'
  angular
      .module('offices.admin',['ngRoute', 'ui.bootstrap', 'login','files',])
      .run(function(Login, $window) {
        Login.check();
      });
})();

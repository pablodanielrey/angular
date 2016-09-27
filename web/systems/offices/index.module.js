(function() {
  'user strict'
  angular
      .module('offices',['ngRoute','login','users','files','fce'])
      .run(function(Login, $window) {
        Login.check();
      });

})();

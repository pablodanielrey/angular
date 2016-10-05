(function() {
  'user strict'
  angular
      .module('assistance',['ngRoute','login','users','files','fce'])
      .run(function(Login, $window) {
        Login.check();
      });

})();

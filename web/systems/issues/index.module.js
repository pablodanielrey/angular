(function() {
  'user strict'
  angular
      .module('issues',['ngRoute','login','users','offices','files','fce'])
      .run(function(Login, $window) {
        Login.check();
      });

})();

(function() {
  'user strict'
  angular
      .module('assistance',['ngRoute','login','users','files','fce', 'offices'])
      .run(function(Login, $window) {
        Login.check();
      });

})();

(function() {
  'user strict'
  angular
      .module('issues',['ngRoute','login','users','offices','files'])
      .run(function(Login) {
        Login.check();
      });

})();

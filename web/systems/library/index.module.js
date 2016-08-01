(function() {
angular
    .module('library',['ngRoute','login'])
    .run(function(Login) {
      Login.check();
    });

})();

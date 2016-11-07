(function() {
  'user strict'
  angular
      .module('offices',['ngRoute', 'login', 'users', 'files', 'fce', 'ngImgCrop'])
      .run(function(Login, $window) {
        Login.check();
      });

})();

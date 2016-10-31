
(function() {
  'use strict';

  angular
    .module('login')
    .controller('IndexLoginCtrl',IndexLoginCtrl);

  IndexLoginCtrl.$inject = ['$rootScope','$scope', 'Login', '$window'];

  function IndexLoginCtrl($rootScope, $scope, Login, $window) {

    activate();
    function activate() {
      // Login.redirect();
    }
  };

})();

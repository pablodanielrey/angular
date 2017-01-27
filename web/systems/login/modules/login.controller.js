(function() {
  'use strict';

  angular
    .module('login')
    .controller('LoginCtrl', LoginCtrl)
    .directive('mooFocusExpression', function($timeout) {
      return {
          link: function(scope, element, attrs) {
            scope.$watch(attrs.mooFocusExpression, function (value) {

                if (attrs.mooFocusExpression) {
                    if (scope.$eval(attrs.mooFocusExpression)) {
                        $timeout(function () {
                            element[0].focus();
                        }, 100); //need some delay to work with ng-disabled
                    }
                }
            });
          }
      };
    });


  LoginCtrl.$inject = ['$scope','$window', '$interval', '$location', 'Login',  '$q', '$timeout'];

  function LoginCtrl($scope, $window, $interval, $location, Login, $q, $timeout) {

      $scope.$on('wamp.open', function(event) {
        Login.login("31073351", "Hola1024").then(
          function (conn) {

            Login.getRegisteredSystems(conn).then(
            function(systems) {
                console.log(systems);

              },
              function(err) {
                console.log(err);
              });
          },
          function(err) {
            console.log(err);
          });
      });

  };

})();

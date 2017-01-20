 (function() {
    'use strict';

    angular
        .module('users')
        .controller('ListUsersCtrl', ListUsersCtrl);

    ListUsersCtrl.$inject = ['$scope', 'Login', 'Users', 'Utils'];


    function ListUsersCtrl($scope, Login, Users, Utils) {

      $scope.$on('wamp.open', function(event, args) {
            Users.findAll().then(
              function(r){
                 console.log(r)
                  $scope.rows = r;
                }
            )
      });


    }
})();

 (function() {
    'use strict';

    angular
        .module('users')
        .controller('ListUsersCtrl', ListUsersCtrl);

    ListUsersCtrl.$inject = ['$scope', 'Login', 'Users', 'Utils', "$timeout"];


    function ListUsersCtrl($scope, Login, Users, Utils, $timeout) {


      $scope.loadUser = function(){
         Users.findAll().then(
        function(r){
           console.log(r)
            $scope.rows = r;
          }
      )
    }


      $timeout($scope.loadUser, 500);

    }
})();

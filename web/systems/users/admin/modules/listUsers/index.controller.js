 (function() {
    'use strict';

    angular
        .module('users')
        .controller('ListUsersCtrl', ListUsersCtrl);

    ListUsersCtrl.$inject = ['$scope', '$timeout', 'Users'];


    function ListUsersCtrl($scope, $timeout, Users) {

      $scope.searchDisabled = true; //flag para habilitar formulario de busqueda
      $scope.search = null; //busqueda
      $scope.searchMessage = null; //Mensaje

      $scope.users = []; //lista de usuarios

      var activate = function(){
        $scope.searchDisabled = false;
      }

      $scope.searchUsers = function(){

        if($scope.search.length > 3){
          $scope.searchDisabled = true;
          $scope.searchMessage = "Buscando";

          Users.search($scope.search).then(
            function(ids){
                Users.findByIds(ids).then(
                  function(users){
                    $scope.searchMessage = null; //Mensaje
                    $scope.users = users;
                    $scope.$apply();
                  }
                )
            }
          )
        }
      }

      $timeout(activate, 0);

    }
})();

 (function() {
    'use strict';

    angular
        .module('offices.admin')
        .controller('ListUsersCtrl', ListUsersCtrl);

    ListUsersCtrl.$inject = ['$scope', '$timeout', 'OfficesAdmin'];


    function ListUsersCtrl($scope, $timeout, OfficesAdmin) {

      $scope.searchDisabled = true; //flag para habilitar formulario de busqueda
      $scope.search = null; //busqueda
      $scope.searchMessage = null; //Mensaje

      $scope.users = []; //lista de usuarios

      var init = function(){
        $scope.searchDisabled = false;
      }

      $scope.searchUsers = function(){

        if($scope.search.length > 3){
          $scope.searchDisabled = true;
          $scope.searchMessage = "Buscando";

          OfficesAdmin.searchUsers($scope.search).then(
            function(users){
              $scope.searchMessage = null; //Mensaje
              $scope.users = users;
              $scope.$apply();
            }
          )
        }
      }

      $timeout(init, 500); //TODO reemplazar por evento de inicializacion de Login

    }
})();

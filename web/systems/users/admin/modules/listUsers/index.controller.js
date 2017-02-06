 (function() {
    'use strict';

    angular
        .module('users.admin')
        .controller('ListUsersCtrl', ListUsersCtrl);

    ListUsersCtrl.$inject = ['$scope', '$timeout', '$routeParams', 'UsersAdmin', '$location'];


    function ListUsersCtrl($scope, $timeout, $routeParams, UsersAdmin, $location) {

      $scope.searchDisabled = true; //flag para habilitar formulario de busqueda
      $scope.search = null; //busqueda
      $scope.searchMessage = null; //Mensaje

      $scope.users = []; //lista de usuarios

      var init = function(){
        $scope.searchDisabled = false;
        var params = $routeParams;
        $scope.search = params.search;
        if ('search' in params) {
          $scope.searching();
        }
      }

      $scope.searchUsers = function(){
        if($scope.search.length > 3){
          $location.path('/listUsers/' + $scope.search)
        }
      }

      $scope.searching = function() {

        $scope.searchDisabled = true;
        $scope.searchMessage = "Buscando";


        UsersAdmin.search($scope.search).then(
          function(users){
            $scope.searchMessage = null; //Mensaje
            $scope.users = users;
            $scope.$apply();
          }
        )

      }

      $timeout(init, 500); //TODO reemplazar por evento de inicializacion de Login

    }
})();

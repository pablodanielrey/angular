(function() {
    'use strict';

    angular
        .module('issues')
        .controller('OrdersCreateCtrl', OrdersCreateCtrl);

    OrdersCreateCtrl.$inject = ['$scope', '$location', 'Login', 'Issues'];

    /* @ngInject */
    function OrdersCreateCtrl($scope, $location,  Login, Issues) {
        var vm = this;

        // variables del modelo
        vm.model = {
          user: null,
          users: []
        }



        // variables de la vista
        vm.view = {

        }

        // métodos


        activate();
        vm.cancel = cancel;
        vm.searchUsers = searchUsers;

        function searchUsers(regex) {

          Issues.searchUsers(regex).then(
            function(users) {
              vm.model.users = users;              
            }, function(error) {
              console.log(error);
            }
          );
        }


        function activate() {
          vm.model.userId = Login.getCredentials()['userId'];
          searchUsers('walt');
        }

        function cancel() {
          $location.path('/orders');
        }


    }
})();

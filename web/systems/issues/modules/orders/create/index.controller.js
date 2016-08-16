(function() {
    'use strict';

    angular
        .module('issues')
        .controller('OrdersCreateCtrl', OrdersCreateCtrl);

    OrdersCreateCtrl.$inject = ['$scope', '$timeout', '$filter', 'Login', 'Issues', 'Users'];

    /* @ngInject */
    function OrdersCreateCtrl($scope, $timeout, $filter,  Login, Issues, Users) {
        var vm = this;

        // variables del modelo
        vm.model = {

        }



        // variables de la vista
        vm.view = {

        }

        // métodos


        activate();

        function activate() {
          vm.model.userId = Login.getCredentials()['userId']


        }

/* ************************************************************************ */
/* ********************** INICIALIZACION ********************************** */
/* ************************************************************************ */

        function initializeView() {

        }

        function initializeModel() {

        }


    }
})();

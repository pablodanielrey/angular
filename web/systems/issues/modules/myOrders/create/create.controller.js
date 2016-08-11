(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersCreateCtrl', MyOrdersCreateCtrl);

    MyOrdersCreateCtrl.$inject = ['$scope', '$timeout', '$filter', 'Login', 'Issues', 'Users', 'Offices', 'Files'];

    /* @ngInject */
    function MyOrdersCreateCtrl($scope, $timeout, $filter, Login, Issues, Users, Offices, Files) {
        var vm = this;

        vm.model = {
          issue: null,
          description: '',
          files: [],
          selectedOffice: null,
          searchOffice: {name: ''},
          selectedOffice: null,
          searchOffice: {name: ''},
          subject: '',
        };

        vm.view = {
          style2: '',
          styles2: ['', 'buscarOficina', 'buscarArea', 'buscarConsulta', 'verMisOficinas', 'pantallaMensaje'],
        };




        activate();


        function activate() {
          
        }




    }
})();

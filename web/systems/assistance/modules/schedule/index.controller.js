(function() {
    'use strict';

    angular
        .module('mainApp')
        .controller('ScheduleController', ScheduleController);

    ScheduleController.$inject = ['$scope', 'Login', 'Assistance'];

    /* @ngInject */
    function ScheduleController($scope, Login, Assistance) {
        var vm = this;

        // Variables
        vm.model = {

        }

        vm.view = {
          styles: ['pantallaUsuario', 'pantallaJefe'],
          style: null,
          styles2: ['', 'pantallaUsuarios', 'nuevoHorarioSemanal', 'nuevoHorarioEspecial'],
          style2: null,
          styles3: ['', 'pantallaMensaje'],
          style3: null,
          styles4: ['', 'procesando', 'procesado', 'errorDeSistema'],
          style4: null
        }
        // Funciones
        vm.activate = activate;
        vm.initView = initView;


        /////////////////////////////////////////
        activate();

        function activate() {
          initView();
        }

        function initView() {
          vm.view.style = vm.view.styles[1];
          vm.view.style2 = vm.view.styles2[0];
          vm.view.style3 = vm.view.styles3[0];
          vm.view.style4 = vm.view.styles4[0];          
        }

    }
})();


(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('JustificationsCtrl',JustificationsCtrl);

    JustificationsCtrl.$inject = ['$scope', 'Assistance', 'Users', '$timeout', 'Login', '$window', 'Offices', '$filter'];

    function JustificationsCtrl($scope, Assistance, Users, $timeout, Login, $window, Offices, $filter) {
        var vm = this;

        vm.view = {
          style: 'pantallaPrincipal',
          newJustification: newJustification,
          back:back,
          backList:backlist,
          save:save,
          listJustification:listJustification,
          editJustification:editJustification,
        }


        function newJustification() {
          vm.view.style = 'pantallaEdicion nuevaJustificacion';
        }

        function back() {
          vm.view.style = 'pantallaPrincipal';
        }
        function save() {
          vm.view.style = 'pantallaPrincipal';
        }

        function listJustification() {
          vm.view.style =  'pantallaEdicion listaDeJustificaciones';
        }

        function backlist() {
          vm.view.style =  'pantallaEdicion listaDeJustificaciones';
        }

        function editJustification() {
          vm.view.style =  'pantallaDerecha EditarJustificacion';
        }


    }


})();

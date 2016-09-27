(function() {
    'use strict';

    angular
        .module('offices')
        .controller('OfficesCtrl', OfficesCtrl);

    OfficesCtrl.$inject = ['$scope', 'Login'];

    /* @ngInject */
    function OfficesCtrl($scope, Login) {
        var vm = this;

        vm.model = {
          userId: null,
          offices: [],
          users: [],
          office: null
        }

        vm.loadOffices = loadOffices;
        vm.remove = remove;
        vm.create = create;
        vm.addUser = addUser;
        vm.removeUser = removeUser;
        vm.selectOffice = selectOffice;

        $scope.$on('wamp.open', function(event, args) {
          vm.model.privateTransport = Login.getPrivateTransport();
          activate();
        });

        activate();


        function activate() {
          if (Login.getPrivateTransport() == null) {
            return;
          }

          vm.model.userId = Login.getCredentials().userId;
          vm.loadOffices();
        }

        function loadOffices() {
          vm.model.offices = [ {name: 'Dirección de Tecnología y Servicios Informáticos', users:[]}, {name: 'Dirección de Mantenimiento y Servicios Generales ', users:[]}, {name: 'Soporte Técnico', users:[]}, {name: 'Dirección de Económico Financiero ', users:[]},{name: 'Dirección de Despacho', users:[]}];
          vm.model.users = [ {name: 'Emanuel Pais'}, {name: 'Ivan Castañeda'}, {name: 'Walter Blanco'}];
        }

        function create() {
          vm.model.office = {};
          vm.model.office.users = [];
          vm.model.office.name = '';
        }

        function selectOffice(office) {
          vm.model.office = office;
          console.log(vm.model.office.name);
        }

        function remove(office) {
          var index = vm.model.offices.indexOf(office);
          if (index > -1) {
              vm.model.offices.splice(index, 1);
          }
        }

        function addUser(user) {
          var index = vm.model.users.indexOf(user);
          if (index > -1) {
              vm.model.users.splice(index, 1);
          }
          vm.model.office.users.push(user);
        }

        function removeUser(user) {
          var index = vm.model.office.users.indexOf(user);
          if (index > -1) {
              vm.model.office.users.splice(index, 1);
          }
          vm.model.users.push(user);
        }
    }
})();

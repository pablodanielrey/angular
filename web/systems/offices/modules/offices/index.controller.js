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
          offices: []
        }

        vm.loadOffices = loadOffices;
        vm.remove = remove;
        vm.create = create;

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
          vm.model.offices = [ {name: 'Dirección de Tecnología y Servicios Informáticos'}, {name: 'Soporte'}, {name: 'Desarrollo'}];
        }

        function create() {
          console.log('create');
        }

        function remove(office) {
          var index = vm.model.offices.indexOf(office);
          if (index > -1) {
              vm.model.offices.splice(index, 1);
          }
        }
    }
})();

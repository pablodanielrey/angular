(function() {
    'use strict';

    angular
        .module('offices')
        .controller('OfficesCtrl', OfficesCtrl);

    OfficesCtrl.$inject = ['$scope', 'Login', 'Offices'];

    /* @ngInject */
    function OfficesCtrl($scope, Login, Offices) {
        var vm = this;

        vm.model = {
          userId: null,
          offices: [],
          users: [],
          dictUsers: {},
          displayUsers: [],
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
          vm.model.users = [{id: 1, name: 'Emanuel Pais'}, {id: 2, name: 'Ivan Castañeda'}, {id:3, name: 'Walter Blanco'}];
          vm.model.dictUsers = {1: vm.model.users[0],
                                2: vm.model.users[1],
                                3: vm.model.users[2]};
        }

        vm.searchUsers = searchUsers;
        function searchUsers(text) {
          /*if (vm.view.searching) {
            return
          }*/
          if (text.length < 5) {
            vm.view.searching = false;
            return;
          }
          // vm.view.searching = true;
          Offices.searchUsers(text).then(
            function(users) {
              $scope.$apply(function() {
                // vm.view.searching = false;
                vm.model.users = users;
                vm.model.displayUsers = users.slice(0);
                if (vm.model.office == null || vm.model.office.users == null || vm.model.office.users === undefined) {
                  return;
                }
                removeDisplayUsers();
              });
            }, function(error) {
              // messageError(error);
              console.log(error);
            }
          );
        }

        function removeDisplayUsers() {
          for (var i = 0; i < vm.model.office.users.length; i++) {
            var j = 0;
            var userId = vm.model.office.users[i].id;
            while(j < vm.model.displayUsers.length) {
              if (vm.model.displayUsers[j].id == userId) {
                removeItem(vm.model.displayUsers, vm.model.displayUsers[j]);
              }
              j = j + 1;
            }
          }
        }

        function create() {
          vm.model.office = {};
          vm.model.office.users = [];
          vm.model.office.name = '';
          vm.model.displayUsers = vm.model.users.slice(0);
        }

        function selectOffice(office) {
          vm.model.office = office;
          vm.model.displayUsers = vm.model.users.slice(0);
          removeDisplayUsers();
        }

        function removeItem(array, item) {
          var index = array.indexOf(item);
          if (index > -1) {
              array.splice(index, 1);
          }
        }

        function remove(office) {
          removeItem(vm.model.offices, office);
        }

        function addUser(user) {
          removeItem(vm.model.displayUsers, user);
          vm.model.office.users.push(user);
        }

        function removeUser(user) {
          removeItem(vm.model.office.users, user);
          vm.model.displayUsers.push(user);
        }
    }
})();

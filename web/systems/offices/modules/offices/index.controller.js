(function() {
    'use strict';

    angular
        .module('offices')
        .controller('OfficesCtrl', OfficesCtrl);

    OfficesCtrl.$inject = ['$scope', 'Login', 'Offices', 'Utils', '$timeout', 'Users'];

    ///////// funciones utilitarias genéricas //////////////

    function removeItem(array, item) {
      var index = array.indexOf(item);
      if (index > -1) {
          array.splice(index, 1);
      }
    }


    /* @ngInject */
    function OfficesCtrl($scope, Login, Offices, Utils, $timeout, Users) {
        var vm = this;

        vm.view = {
          style: '',
          styles: ['pantallaPrincipal', 'pantallaEdicion', 'pantallaUsuarios'],
          style2:'',
          styles2: ['', 'mensajes'],
          style3: '',
          styles3: ['mensajeEliminarOficina', 'mensajeGuardado', 'mensajeCargando']
        };

        vm.model = {
          userId: null,
          offices: [],
          users: [],
          displayUsers: [],
          office: null,
          officeTypes: [],
          selectedType: null
        }

        vm.getOfficeTypes = getOfficeTypes;
        vm.remove = remove;
        vm.create = create;
        vm.addUser = addUser;
        vm.removeUser = removeUser;
        vm.displayRemove = displayRemove;
        vm.selectOffice = selectOffice;
        vm.searchUsers = searchUsers;
        vm.saveOffice = saveOffice;
        vm.cancel = cancel;

        $scope.$on('wamp.open', function(event, args) {
          vm.model.privateTransport = Login.getPrivateTransport();
          activate();
        });

        activate();

        function activate() {
          if (Login.getPrivateTransport() == null) {
            return;
          }

          subscribeEvents();
          vm.view.style = vm.view.styles[0];
          vm.view.style2 = vm.view.styles2[0];

          vm.model.selectedType = null;
          vm.model.userId = Login.getCredentials().userId;
          vm.getOfficeTypes();
          loadAllOffices();
        }

        function subscribeEvents() {
          Offices.subscribe('offices.persist_event', function(params) {
            var id = params[0];
            $scope.$apply(function() {
              loadAllOffices();
            });
          });

          Offices.subscribe('offices.remove_event', function(params) {
            var id = params[0];
            $scope.$apply(function() {
              loadAllOffices();
            });
          });
        }




        function loadAllOffices() {
          Utils.findAll().then(
              function(offices) {
                vm.model.offices = offices;
              }, function(error) {
                console.error(error);
              }
          );
        }


        // TODO: obtiene el listado de tipos de oficinas
        function getOfficeTypes() {
          vm.model.officeTypes = [];
          vm.model.selectedType = null;
          Utils.getOfficeTypes().then(
            function(types) {
              vm.model.officeTypes = types;
              vm.model.selectedType = vm.model.officeTypes[0];
            }, function(error) {
              // messageError(error);
              console.log(error);
            }
          );
        }

        function searchUsers(text) {
          if (text.length < 3) {
            vm.view.searching = false;
            return;
          }

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
          if (vm.model.office.users == undefined || vm.model.office.users == null) {
            return;
          }
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

        function cancel() {
          vm.view.style = vm.view.styles[0];
        }


        function create() {
          vm.view.style = vm.view.styles[1];

          vm.model.office = {};
          vm.model.office.id = null;
          vm.model.office.name = '';
          vm.model.office.telephone = '';
          vm.model.office.number = '';
          vm.model.office.email = '';
          vm.model.displayUsers = vm.model.users.slice(0);
        }

        function saveOffice() {
          var ok = true;

          if (vm.model.office.name.trim() == '') {
            ok = false;
            window.alert("Debe completar el nombre de la oficina");
          }

          if (vm.model.office.type == null) {
            ok = false;
            window.alert('Debe seleccionar el tipo de la oficina');
          }

          if (!ok) {
            return;
          }

          Utils.persist(vm.model.office).then(
            function(response) {
              $scope.$apply(function() {
                vm.view.style2 = vm.view.styles2[1];
                vm.view.style3 = vm.view.styles3[1];
                $timeout(function () {
                    vm.view.style2 = vm.view.styles2[0];
                    vm.view.style = vm.view.styles[0];
                }, 1000);


              })
            }, function(error) {
              console.error(error);
            }
          )
        }

        function selectOffice(office) {
          vm.view.style = vm.view.styles[1];
          vm.model.office = office;

          // TODO: reever código. implemente el metodo para obtener los usuarios de las oficinas.
          vm.model.officeUsers = [];
          Offices.findUsersByIds(vm.model.office.users).then(function(users) {
            $scope.$apply(function() {
              vm.model.officeUsers = users;
            });
          }, function(err) {
            console.log(err);
          });

          // ----------------------------------------------------

          // selecciono el tipo de oficina del arreglo de officesTypes para que se la misma instancia de typeOffice
          if (office.type != undefined && office.type != null) {
            for(var i = 0; i < vm.model.officeTypes.length; i++) {
              if (vm.model.officeTypes[i].value == office.type.value) {
                office.type = vm.model.officeTypes[i];
                break;
              }
            }
          }

          // selecciono el padre
          vm.model.office.parentObj = null;
          if (office.parent != null && office.parent.trim() != '') {
            for (var i = 0; i < vm.model.offices.length; i++) {
              if (office.parent == vm.model.offices[i].id) {
                vm.model.office.parentObj = vm.model.offices[i];
                break;
              }
            }

          }

          vm.model.displayUsers = vm.model.users.slice(0);
          removeDisplayUsers();
        }




        function displayRemove(office) {
          vm.model.office = office;
          vm.view.style2 = vm.view.styles2[1];
          vm.view.style3 = vm.view.styles3[0];
        }

        vm.cancelRemove = cancelRemove;
        function cancelRemove() {
          vm.view.style2 = vm.view.styles2[0];
        }

        function remove() {
          Utils.remove(vm.model.office).then(
            function(id) {
              vm.view.style2 = vm.view.styles2[0];
            }, function(error) {
              console.error(error);
            }
          );
        }


        //// manejo de usuarios de una oficina ///////

        function addUser(user) {
          removeItem(vm.model.displayUsers, user);
          vm.model.officeUsers.push(user);
          vm.view.style = vm.view.styles[1];
        }

        function removeUser(user) {
          removeItem(vm.model.officeUsers, user);
          vm.model.displayUsers.push(user);
        }

        ////////////////////////
    }
})();

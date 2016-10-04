 (function() {
    'use strict';

    angular
        .module('offices')
        .controller('OfficesCtrl', OfficesCtrl);

    OfficesCtrl.$inject = ['$scope', 'Login', 'Offices', 'Utils', '$timeout', 'Users', 'Files'];

    ///////// funciones utilitarias genéricas //////////////

    function removeItem(array, item) {
      var index = array.indexOf(item);
      if (index > -1) {
          array.splice(index, 1);
      }
    }


    /* @ngInject */
    function OfficesCtrl($scope, Login, Offices, Utils, $timeout, Users, Files) {
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
          offices: [],
          office: null,
          officeUsers: [],

          usersToAdd: [],                 // usuarios a agregar a la oficina
          officeTypes: [],
          selectedType: null
        }

        vm.aux = {
          searchTimer: null               // timer usado en la directiva de usuarios para buscar un nuvo usuario
        }

        ////////////////// directiva de lista de oficinas //////////
        vm.getOfficeTypes = getOfficeTypes;
        vm.remove = remove;
        vm.create = create;
        vm.selectOffice = selectOffice;
        /////////////////////////////////////////

        /////// pantalla de edición de oficina ////////////
        vm.cancel = cancel;
        vm.addUser = addUser;
        vm.saveOffice = saveOffice;
        //////////////////////////////////////////

        /////// directiva de lista de usuarios ////////////
        vm.searchUsers = searchUsers;
        vm.showUsersToAdd = showUsersToAdd;
        vm.removeUser = removeUser;
        //////////////////////////////////////////////////////

        ////////// visaules ///////////////
        vm.getUserPhoto = getUserPhoto;
        vm.displayRemove = displayRemove;
        //////////////////////


        function getUserPhoto(user) {
          if (user == null || user.photo == null) {
            var img = user != null && "genre" in user && user.genre != null && (user.genre.toLowerCase() == 'femenino' || user.genre.toLowerCase() == 'mujer') ? "img/avatarWoman.jpg" : "img/avatarMan.jpg";
            return img;
          } else {
            return Files.toDataUri(user.photo);
          }
        }





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
          //vm.model.userId = Login.getCredentials().userId;
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


        ////////////////////////////////// listado de oficinas //////////////////////////////////////////

        function onOfficeTypesSelected() {
            // nada
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
              //vm.model.selectedType = vm.model.officeTypes[0];
              vm.model.selectedType = '';
            }, function(error) {
              console.log(error);
            }
          );
        }

        function create() {
          vm.view.style = vm.view.styles[1];

          vm.model.office = {};
          vm.model.office.id = null;
          vm.model.office.name = '';
          vm.model.office.telephone = '';
          vm.model.office.number = '';
          vm.model.office.email = '';
          vm.model.office.users = [];

          vm.model.officeUsers = [];
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

        ////////////////////////////////////////////////////////////



        /////////////// edicion/creación de una oficina ///////////////////

        /*
          Actualiza/crea la oficina.
          para actualizar solo se tiene en cuenta el objeto seleccionado:
            vm.model.office
          y se crearán las designaciones "cumpliendo funciones" de los usuarios indicados:
            vm.model.office.users --> uids de los usuarios que quedan en la oficina.
        */
        function saveOffice() {
          var ok = true;

          if (vm.model.office.name.trim() == '') {
            window.alert("Debe completar el nombre de la oficina");
            return;
          }

          if (vm.model.office.type == null) {
            window.alert('Debe seleccionar el tipo de la oficina');
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
          vm.model.office = angular.copy(office);

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
          if (vm.model.office.type != undefined && vm.model.office.type != null) {
            for(var i = 0; i < vm.model.officeTypes.length; i++) {
              if (vm.model.officeTypes[i].value == vm.model.office.type.value) {
                vm.model.office.type = vm.model.officeTypes[i];
                break;
              }
            }
          }

          // selecciono el padre
          vm.model.office.parentObj = null;
          if (vm.model.office.parent != null && vm.model.office.parent.trim() != '') {
            for (var i = 0; i < vm.model.offices.length; i++) {
              if (vm.model.office.parent == vm.model.offices[i].id) {
                vm.model.office.parentObj = vm.model.offices[i];
                break;
              }
            }

          }
        }

        function cancel() {
          vm.view.style = vm.view.styles[0];
           loadAllOffices();
        }

        /////////////////////////////////////////////////////////////









        /////////////// manejo de usuarios de una oficina //////////////////////

        /*
          muestra la pantalla de lista de usuarios para agregar a la oficina.
          la busqueda se realiza en searchUsers disparada por un cambio en el buscar.
        */
        function showUsersToAdd() {
          vm.view.style = vm.view.styles[2];
        }

        /*
          Busca usuarios a partir de una expresión regular.
          implementa un timer para no busar con cada cambio que se neceiste.
          el tema del timer usa:
            vm.aux.searchTimer ---> timer para el buscado.

          actualizar :
            vm.view.searching ---- true|false
            vm.aux.searchTimer  -- timer del proceso a buscar usuarios
        */
        function searchUsers(text) {
          if (text.length < 3) {
            // menos de 3 letras no se busca
            return;
          }

          if (vm.aux.searchTimer != null) {
            $timeout.cancel(vm.aux.searchTimer);
          }
          vm.aux.searchTimer = $timeout(function () {
            vm.aux.searchTimer = null;
            vm.view.style2 = vm.view.styles2[1];
            vm.view.style3 = vm.view.styles3[2];

            Offices.searchUsers(text).then(
              function(users) {
                $scope.$apply(function() {
                  vm.view.style2 = vm.view.styles2[0];
                  _processUsersFound(users);
                });
              }, function(error) {
                console.log(error);
              }
            );
          }, 2000);
        }

        /*
          Procesa los usaurios encontrados desde el searchUsers(text)
          para actualziar correctamente todas las variables dependeintes de los usuarios que estan o no dentro de la oficina.
          hay que actualizar las variables :

              vm.model.usersToAdd --- > usuarios que se muestran en la listad  --- esta es la que setea!!!
              vm.model.officeUsers ---> usuarios mostrados dentro de la oficina
              vm.model.office.users --> ids de los usuarios de las personas
        */
        function _processUsersFound(users) {
          vm.model.usersToAdd = users.filter(function(u) {
            for (var i = 0; i < vm.model.office.users.length; i++) {
              if (u.id == vm.model.office.users[i].id) {
                return false;
              }
            }
            return true;
          });
        }

        /*
          Llamada desde la directiva para agregar un usuario a la oficina
        */
        function addUser(user) {
          //vm.view.style = vm.view.styles[2];

          // elimino el usuario de la lista.
          vm.model.usersToAdd = vm.model.usersToAdd.filter(function(u) {
            if (u.id == user.id) {
              return false;
            }
            return true;
          });

          // lo agrego a la lista de usuarios de la oficina
          vm.model.officeUsers.push(user);
          vm.model.office.users.push(user.id);
        }

        /*
          Llamada desde la edición de la oficina para eliinar un usuario de la oficina.
        */
        function removeUser(user) {
          //vm.view.style = vm.view.styles[2];

          // elimino el usuario de la lista.
          vm.model.officeUsers = vm.model.officeUsers.filter(function(u) {
            if (u.id == user.id) {
              return false;
            }
            return true;
          });
          vm.model.office.users = vm.model.office.users.filter(function(id) {
            if (id == user.id) {
              return false;
            }
            return true;
          });

          // lo agrego a la lista de usuarios a agregar en el caso de que el filtro lo permita.
          var temp = angular.copy(vm.model.usersToAdd);
          temp.push(user);
          _processUsersFound(temp);
        }


        ////////////////////////
    }
})();

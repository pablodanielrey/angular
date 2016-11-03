(function() {
    'use strict';

    angular
        .module('assistance')
        .controller('EditHoursSchCtrl', EditHoursSchCtrl);

    EditHoursSchCtrl.$inject = ['$scope', 'Users', 'Login', '$routeParams', '$q', '$timeout', '$location'];

    /* @ngInject */
    function EditHoursSchCtrl($scope, Users, Login, $routeParams, $q, $timeout, $location) {
        var vm = this;

        vm.model = {
          date: null,
          selectedPerson: null,
          schedules: [],

          users: [],
          user: null
        }

        vm.view = {
          style:'',
          profileAdmin: 'usuarioAdmin',
          profileUser: 'usuarioNormal',
          displayEdit: 'pantallaEdicion nuevoHorarioSemanalSerenos',
          saveMessage: 'pantallaEdicion nuevoHorarioSemanal mensajes mensajeGuardado',
          loadingMessage: 'pantallaEdicion nuevoHorarioSemanal mensajes mensajeCargando',
          errorMessage: 'pantallaEdicion nuevoHorarioSemanal mensajes mensajeError',
          profile: 'user',
          activate: false
        }

        vm.getUserPhoto = getUserPhoto;
        vm.displayEditSch = displayEditSch;
        vm.selectUser = selectUser;
        vm.styleItem = styleItem;

        vm.back = back;
        vm.save = save;
        vm.removeSched = removeSched;
        vm.addSched = addSched;

        $scope.$on('wamp.open', function(event, args) {
          activate();
        });

        activate();

        function activate() {
          if (vm.view.activate || Login.getPrivateTransport() == null) {
            return;
          }
          vm.view.activate = true;

          var params = $routeParams;
          if ('personId' in params) {
            vm.model.selectedPerson = params.personId;
          } else {
            vm.model.selectedPerson =  Login.getCredentials()['userId'];
          }

          loadProfile().then(function() {
              vm.displayEditSch()
          });

          loadUsers();
          loadUser();
          vm.model.date = new Date();
        }

        /* **************************************************************************************************
                                            MANEJO VISUAL
        * ************************************************************************************************ */

        function displayEditSch() {
          var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
          vm.view.style = style + ' ' + vm.view.displayEdit;
        }

        function displayMessageSave() {
          var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
          $timeout(function () {
            vm.view.style = style + ' ' + vm.view.saveMessage;
          });
        }

        function displayMessageLoading() {
          var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
          $timeout(function () {
            vm.view.style = style + ' ' + vm.view.loadingMessage;
          });
        }

        function getUserPhoto() {
          return (vm.model.user == null || !'photoSrc' in vm.model.user) ? 'img/avatarMan.jpg' : vm.model.user.photoSrc
        }

        function styleItem(sched, index) {
          return (vm.model.schedules.length <= 1) ? 'primerHorario' : (index == 0) ? 'otroHorario primero' : 'otroHorario';
        }

        function back() {
          $location.path("/schedules/" + vm.model.selectedPerson);
        }


        /* **************************************************************************************************
                                            MANEJO DE PERFIL DE USUARIO
        * ************************************************************************************************ */

        function loadProfile() {
          var d = $q.defer();
          // aca deberia hacer la llamada al servidor
          vm.view.profile = "admin";

          var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
          vm.view.style = style + ' ' + vm.view.displayListUsers;
          d.resolve();

          return d.promise;
        }

        function loadUser() {
          vm.model.user = null;
          Users.findById([vm.model.selectedPerson]).then(Users.findPhotos).then(Users.photoToDataUri).then(function(users) {
            $timeout(function() {
              vm.model.user = (users.length <= 0) ? null : users[0];
            },0);
          }, function(err) {
            console.log(err);
          })
        }
        /* **************************************************************************************************
                                            MANEJO DE SCHEDULES
        * ************************************************************************************************ */

        $scope.$watch('vm.model.date', function(newVal, oldVal) {
          if (newVal == null && oldVal == null) {
            return;
          }
          if (newVal == null) {
            vm.model.date = oldVal;
            return;
          }

          loadSchedules();
        });

        function loadSchedules() {
          var start = new Date(); start.setHours(21); start.setMinutes(0); start.setSeconds(0); start.setMilliseconds(0);
          vm.model.schedules.push({day:"2", start: start, hours: 25});
          start = new Date(); start.setHours(15); start.setMinutes(0); start.setSeconds(0); start.setMilliseconds(0);
          vm.model.schedules.push({day:"4", start: start, hours: 30});
        }

        function removeSched(sched) {
          var index = vm.model.schedules.indexOf(sched);
          vm.model.schedules.splice(index, 1);
        }

        function addSched() {
          var start = new Date(); start.setHours(0); start.setMinutes(0); start.setSeconds(0); start.setMilliseconds(0);
          vm.model.schedules.push({day:"1", start: start, hours: 0});
        }
        /* **************************************************************************************************
                                            MANEJO DE PERSONAS
        * ************************************************************************************************ */

            function loadUsers() {
                vm.model.users = [];
                vm.model.users.push({id:'1', dni: '31381082', name: 'Emanuel Joaquín', lastname: 'Pais', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'2', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'3', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'4', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'5', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'6', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'7', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'8', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'9', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'10', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'11', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'12', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'13', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'14', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'15', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'16', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'17', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
                vm.model.users.push({id:'18', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            }

            function selectUser(user) {
              $location.path("/schedules/" + user.id);
            }

            /* **************************************************************************************************
                                                GUARDAR
            * ************************************************************************************************ */
            function save() {
              vm.view.style = displayMessageLoading();
              $timeout(function () {
                vm.view.style = displayMessageSave();
                $timeout(function () {
                  $location.path("/schedules/" + vm.model.selectedPerson);
                }, 2000);
              }, 2000);
            }
    }
})();

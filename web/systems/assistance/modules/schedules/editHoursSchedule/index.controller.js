(function() {
    'use strict';

    angular
        .module('assistance')
        .controller('EditHoursSchCtrl', EditHoursSchCtrl);

    EditHoursSchCtrl.$inject = ['$scope', 'Users', 'Login', '$routeParams', 'Assistance', '$timeout', '$location'];

    /* @ngInject */
    function EditHoursSchCtrl($scope, Users, Login, $routeParams, Assistance, $timeout, $location) {
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
          saveMessage: 'pantallaEdicion nuevoHorarioSemanalSerenos mensajes mensajeGuardado',
          loadingMessage: 'pantallaEdicion nuevoHorarioSemanalSerenos mensajes mensajeCargando',
          errorMessage: 'pantallaEdicion nuevoHorarioSemanalSerenos mensajes mensajeError',
          profile: 'user',
          activate: false,
          error: ''
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

          loadProfile();
          loadUser();
          vm.model.date = new Date();
        }

        /* **************************************************************************************************
                                            MANEJO VISUAL
        * ************************************************************************************************ */

        function displayEditSch() {
          var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
          $timeout(function() {
            vm.view.style = style + ' ' + vm.view.displayEdit;
          })
        }

        function displayMessageSave() {
          var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
          $timeout(function () {
            vm.view.style = style + ' ' + vm.view.saveMessage;
          });
        }

        function displayMessageError(error) {
          var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
          vm.view.error = error;
          vm.view.style = style + ' ' + vm.view.errorMessage;
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
          Assistance.loadProfile().then(function(profile) {
            _loadProfile(profile);
          }, function(error) {
            displayMessageError(error);
            $timeout(function() {
                _loadProfile(null)
            }, 1500);
          })
        }



        function _loadProfile(profile) {
          vm.view.profile = profile;
          var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
          vm.view.style = style + ' ' + vm.view.displayListUsers;

          vm.displayEditSch();
        }

        function loadUser() {
          vm.model.user = null;
          Users.findById([vm.model.selectedPerson]).then(Users.findPhotos).then(Users.photoToDataUri).then(function(users) {
            $timeout(function() {
              vm.model.user = (users.length <= 0) ? null : users[0];
            },0);
          }, function(err) {
            displayMessageError(error);
            $timeout(function() {
                vm.displayEditSch();
            }, 1500);
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
          displayMessageLoading();
          vm.model.schedules = [];
          Assistance.loadWatcherSchedules(vm.model.date).then(function(schedules) {
            vm.model.schedules = schedules;
            vm.displayEditSch();
          }, function(error) {
            displayMessageError(error);
            $timeout(function() {
                vm.displayEditSch();
            }, 1500);
          })
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


            function selectUser(user) {
              $location.path("/schedules/" + user.id);
            }

            /* **************************************************************************************************
                                                GUARDAR
            * ************************************************************************************************ */
            function _verify() {
              return true;
            }

            function save() {
              if (!_verify()) {
                return;
              }

              vm.view.style = displayMessageLoading();
              Assistance.saveWatcherSchedules(vm.model.schedules).then(function() {
                vm.view.style = displayMessageSave();
                $timeout(function () {
                  $location.path("/schedules/" + vm.model.selectedPerson);
                }, 2000);
              }, function(error) {
                displayMessageError(error);
                $timeout(function() {
                  vm.view.style = vm.view.displayEdit;
                }, 3000)
              });
            }
    }
})();

(function() {
    'use strict';

    angular
        .module('assistance')
        .controller('EditWeeklySchCtrl', EditWeeklySchCtrl);

    EditWeeklySchCtrl.$inject = ['$scope', 'Assistance', 'Users', 'Login', '$routeParams', '$location', '$timeout', '$filter'];

    /* @ngInject */
    function EditWeeklySchCtrl($scope, Assistance, Users, Login, $routeParams, $location, $timeout, $filter) {
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
          displayEdit: 'pantallaEdicion nuevoHorarioSemanal',
          saveMessage: 'pantallaEdicion nuevoHorarioSemanal mensajes mensajeGuardado',
          loadingMessage: 'pantallaEdicion nuevoHorarioSemanal mensajes mensajeCargando',
          errorMessage: 'pantallaEdicion nuevoHorarioSemanal mensajes mensajeError',
          profile: 'user',
          activate: false,
          error: ''
        }

        vm.getUserPhoto = getUserPhoto;
        vm.selectUser = selectUser;
        vm.displayEditWeeklySch = displayEditWeeklySch;
        vm.getHours = getHours;
        vm.back = back;
        vm.save = save;
        vm.removeSched = removeSched;
        vm.clearSched = clearSched;
        vm.addSched = addSched;
        vm.isSplitSchedule = isSplitSchedule;

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
          loadUsers();
          loadUser();
          vm.model.date = new Date();
        }

        /* **************************************************************************************************
                                            MANEJO VISUAL
        * ************************************************************************************************ */

        function displayEditWeeklySch() {
          var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
          $timeout(function () {
            vm.view.style = style + ' ' + vm.view.displayEdit;
          });
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

        function getHours() {
          var totalMillis = 0;
          var dayMillis = 24 * 60 * 60 * 1000;
          for (var i = 0; i < vm.model.schedules.length; i++) {
            var sched = vm.model.schedules[i];
            if (sched.start == null || sched.end == null) {
              continue;
            }
            if (sched.end < sched.start) {
              sched.end.setTime(sched.end.getTime() + dayMillis);
            }
            totalMillis = totalMillis + (sched.end - sched.start);
          }
          return Math.trunc(totalMillis / 1000 / 60 / 60);
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

          vm.displayEditWeeklySch();
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
                vm.displayEditWeeklySch();
            }, 1500);
          })
        }

        /* **************************************************************************************************
                                            MANEJO DE PERSONAS
        * ************************************************************************************************ */

          function loadUsers() {
            Assistance.loadUsers().then(function(users) {
              vm.model.users = users;
            }, function(error) {
              displayMessageError(error);
              $timeout(function() {
                  vm.displayEditWeeklySch();
              }, 1500);
            })
          }

            function selectUser(user) {
              $location.path("/schedules/" + user.id);
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
              vm.model.schedules = [];
              displayMessageLoading();
              Assistance.loadSchedules(vm.model.date).then(function(schedules) {
                vm.model.schedules = schedules;
                vm.displayEditWeeklySch();
              }, function(error) {
                displayMessageError(error);
                $timeout(function () {
                  vm.displayEditWeeklySch();
                }, 1500);
              })

            }

            function removeSched(sched) {
              var item = vm.model.schedules.indexOf(sched);
              vm.model.schedules.splice(item, 1);
            }

            function clearSched(sched) {
              var item = vm.model.schedules.indexOf(sched);
              if (isSplitSchedule(sched)) {
                removeSched(sched);
              } else {
                sched.start = null;
                sched.end = null;
              }
            }

            function isSplitSchedule(sched) {
              var item = vm.model.schedules.indexOf(sched);
              return (item > 0 && sched.date != null && sched.date.getDay() == vm.model.schedules[item - 1].date.getDay())
            }

            function addSched(sched) {
              if (sched.start == null || sched.end == null) {
                return;
              }

              vm.model.schedules.push({date: sched.date, start: null, end: null, style: 'horarioCortado'});
              vm.model.schedules = $filter('orderBy')(vm.model.schedules, 'date', false);
              console.log(vm.model.schedules);
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
              Assistance.saveSchedules(vm.model.schedules).then(function() {
                vm.view.style = displayMessageSave();
                $timeout(function () {
                  $location.path("/schedules/" + vm.model.selectedPerson);
                }, 2000);
              }, function(error) {
                displayMessageError(error);
                $timeout(function() {
                  vm.view.displayEditWeeklySch;
                }, 3000)
              });
            }
    }
})();

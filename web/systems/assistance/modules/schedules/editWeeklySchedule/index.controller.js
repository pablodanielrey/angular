(function() {
    'use strict';

    angular
        .module('assistance')
        .controller('EditWeeklySchCtrl', EditWeeklySchCtrl);

    EditWeeklySchCtrl.$inject = ['$scope', 'Assistance', 'Users', 'Login', '$routeParams', '$location', '$timeout', '$q', '$filter'];

    /* @ngInject */
    function EditWeeklySchCtrl($scope, Assistance, Users, Login, $routeParams, $location, $timeout, $q, $filter) {
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
          activate: false
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

          loadProfile().then(function() {
              vm.displayEditWeeklySch()
          });

          loadUsers();
          loadUser();
          vm.model.date = new Date();
        }

        /* **************************************************************************************************
                                            MANEJO VISUAL
        * ************************************************************************************************ */

        function displayEditWeeklySch() {
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
              var dayMillis = 24 * 60 * 60 * 1000;
              for (var i = 0; i < 7; i++) {
                var date = new Date(vm.model.date.getTime() + i * dayMillis);
                if (date.getDay() == 6 || date.getDay() == 0) {
                  vm.model.schedules.push({date: date, start: null, end: null, style: 'horarioNormal'});
                  continue;
                }

                if (date.getDay() == 3) {
                  var start = new Date(date.getTime());
                  var end = new Date(date.getTime());
                  start.setHours(7); start.setMinutes(0); start.setSeconds(0); start.setMilliseconds(0);
                  end.setHours(10); end.setMinutes(30); end.setSeconds(0); end.setMilliseconds(0);
                  vm.model.schedules.push({date: date, start: start, end: end, style: 'horarioNormal'});
                  var start = new Date(date.getTime());
                  var end = new Date(date.getTime());
                  start.setHours(15); start.setMinutes(30); start.setSeconds(0); start.setMilliseconds(0);
                  end.setHours(19); end.setMinutes(0); end.setSeconds(0); end.setMilliseconds(0);
                  vm.model.schedules.push({date: date, start: start, end: end, style: 'horarioCortado'});
                } else {
                  var start = new Date(date.getTime());
                  var end = new Date(date.getTime());
                  start.setHours(8); start.setMinutes(0); start.setSeconds(0); start.setMilliseconds(0);
                  end.setHours(15); end.setMinutes(0); end.setSeconds(0); end.setMilliseconds(0);
                  vm.model.schedules.push({date: date, start: start, end: end, style: 'horarioNormal'});
                }
              }
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

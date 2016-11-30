(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('SchedulesCtrl', SchedulesCtrl);

    SchedulesCtrl.$inject = ['$scope', 'Assistance', 'Users', 'Login', '$routeParams', '$location', '$timeout'];

    function SchedulesCtrl($scope, Assistance, Users, Login, $routeParams, $location, $timeout) {
        var vm = this;
        vm.model = {
          users: [],
          schedulesWeek: [],
          schedules: [],

          selectedPerson: null,
          date: null,
          user: null,
          selected: null
        }

        vm.view = {
          style:'',
          profileAdmin: 'usuarioAdmin',
          profileUser: 'usuarioNormal',
          displayListUsers: 'pantallaUsuarios verHorario',
          displayPerson: 'pantallaEdicion verHorario',
          displayQuestions: 'pantallaEdicion verPreguntaDeHorario',
          displayHistory: 'pantallaHistorial',
          loadingMessage: 'pantallaEdicion verHorario mensajes mensajeCargando',
          errorMessage: 'pantallaEdicion verHorario mensajes mensajeError',
          deleteMessage: 'pantallaEdicion verHorario mensajes mensajeEliminarhorario',
          profile: 'user',
          activate: false,
          error: ''
        }

        vm.selectUser = selectUser;
        vm.getUserPhoto = getUserPhoto;
        vm.displayEditQuestions = displayEditQuestions;
        vm.displaySchedule = displaySchedule;
        vm.displayUsers = displayUsers;
        vm.displayEditWeekSch = displayEditWeekSch;
        vm.displayEditHoursSch = displayEditHoursSch;
        vm.displayEditSpecialSch = displayEditSpecialSch;
        vm.getHours = getHours;
        vm.getContentSchedStyle = getContentSchedStyle;

        vm.displayMessageDelete = displayMessageDelete;
        vm.cancelDelete = cancelDelete;
        vm.removeSchedule = removeSchedule;

        $scope.$on('wamp.open', function(event, args) {
          activate();
        });

        activate();

        function activate() {
          if (vm.view.activate || Login.getPrivateTransport() == null) {
            return;
          }
          vm.view.activate = true;

          vm.model.selected = null;
          var params = $routeParams;
          if ('personId' in params) {
            vm.model.selectedPerson = params.personId;
          } else {
            vm.model.selectedPerson =  Login.getCredentials()['userId'];
          }
          loadProfile();
          loadUser();
          vm.model.date = new Date(); 3
          registerEventManagers();

        }

        /* **************************************************************************************************
                                            EVENTOS
        * ************************************************************************************************ */
        function registerEventManagers() {
          Assistance.subscribe('assistance.remove_schedules_event', function(params) {
            console.log("remove");
          });

          Assistance.subscribe('assistance.add_schedules_event', function(params) {
            var historyId = params[0];
            console.log("add");
          });
        }


    /* **************************************************************************************************
                                        MANEJO VISUAL
    * ************************************************************************************************ */

    function displaySchedule() {
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      $timeout(function () {
        vm.view.style = style + ' ' + vm.view.displayPerson;
      });
    }

    function displayUsers() {
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      vm.view.style = style + ' ' + vm.view.displayListUsers;
    }

    function displayEditQuestions() {
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      vm.view.style = style + ' ' + vm.view.displayQuestions;
    }

    function displayEditWeekSch() {
      $location.path("/weekSchedules/" + vm.model.selectedPerson);
    }

    function displayEditHoursSch()  {
      $location.path("/hoursSchedules/" + vm.model.selectedPerson);
    }

    function displayEditSpecialSch()  {
      $location.path("/specialSchedules/" + vm.model.selectedPerson);
    }

    function getUserPhoto() {
      return (vm.model.user == null || !'photoSrc' in vm.model.user) ? 'img/avatarMan.jpg' : vm.model.user.photoSrc
    }

    function displayMessageLoading() {
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      $timeout(function () {
        vm.view.style = style + ' ' + vm.view.loadingMessage;
      });
    }

    function displayMessageDelete(item) {
      vm.model.selected = item;
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      $timeout(function () {
        vm.view.style = style + ' ' + vm.view.deleteMessage;
      });
    }

    function cancelDelete() {
      vm.model.selected = null;
      displayHistory();
    }

    function displayHisotry() {
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      vm.view.style = vm.view.displayHistory;
    }

    function displayMessageError(error) {
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      vm.view.error = error;
      vm.view.style = style + ' ' + vm.view.errorMessage;
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      $timeout(function () {
        vm.view.style = style + ' ' + vm.view.displayHistory;
      });
    }

    function getHours(schedules) {
      var totalMillis = 0;
      var dayMillis = 24 * 60 * 60 * 1000;

      for (var i = 0; i < schedules.length; i++) {
        var sched = schedules[i];
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

    function getContentSchedStyle() {
      if (vm.model.schedules.length > 0) {
        return (vm.model.schedulesWeek.length > 0) ? '' : 'horarioSemanalEspecial';
      } else {
        return 'horarioSemanalClasico';
      }
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
          _loadProfile(null);
        }, 1500);

      })
    }

    function _loadProfile(profile) {
      vm.view.profile = (profile == null) ? 'user' : profile;
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      vm.view.style = style + ' ' + vm.view.displayListUsers;

      if ('personId' in $routeParams) {
        displaySchedule();
      } else {
        displayUsers();
      }
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
            _loadProfile(vm.view.profile)
        }, 1500);
      })
    }

    /* **************************************************************************************************
                                        MANEJO DE PERSONAS
    * ************************************************************************************************ */


      function selectUser(user) {
        if (user.id == vm.model.selectedPerson) {
          vm.displaySchedule();
        } else {
          $location.path("/schedules/" + user.id);
        }
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

        function _parseSchedule(sc) {
          if (sc.schedule == null || sc.schedule.start == null || sc.schedule.end == null) {
            return null;
          }
          // getDay() => [Sunday, Monday, ..., Saturday]
          var sortDay = [6, 0, 1, 2, 3, 4, 5];
          var date = new Date(sc.date);
          var weekday = sortDay[date.getDay()];

          var millisStart = sc.schedule.start * 1000;
          var start = new Date(date.getTime() + millisStart);

          var millisEnd =  sc.schedule.end * 1000;
          var end = new Date(date.getTime() + millisEnd);

          var hours = Math.trunc((end - start) / 1000 / 60 / 60);
          return {date: date, weekday:weekday, start: start, end: end, hours: hours}
        }

        function loadSchedules() {
          vm.model.schedules = [];
          vm.model.schedulesWeek = [];
          displayMessageLoading();
          Assistance.loadSchedules(vm.model.selectedPerson, vm.model.date, true).then(function(schedules) {
            for (var i = 0; i < schedules.length; i++) {
              var sc = _parseSchedule(schedules[i]);
              if (sc == null) {
                continue;
              }
              if (sc.hours < 24) {
                vm.model.schedulesWeek.push(sc);
              } else {
                vm.model.schedules.push(sc);
              }
            }
            vm.displaySchedule();
          }, function(error) {
            displayMessageError(error);
            $timeout(function () {
              vm.displayEditWeeklySch();
            }, 1500);
          })

        }



        function removeSchedule() {
          displayMessageLoading();
          Assistance.removeScheduleHistory(vm.model.selected).then(function(id) {
            $timeout(function () {
              displayHisotry();
            });
          }, function(error) {
            displayMessageError(error);
            $timeout(function () {
              displayHisotry();
            }, 1500);
          })

        }


    }
})();

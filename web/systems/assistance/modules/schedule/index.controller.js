(function() {
    'use strict';

    angular
        .module('mainApp')
        .controller('ScheduleController', ScheduleController);

    ScheduleController.$inject = ['$scope', 'Login', 'Users', 'Assistance', 'Office', '$filter', '$timeout'];

    /* @ngInject */
    function ScheduleController($scope, Login, Users, Assistance, Office, $filter, $timeout) {
        var vm = this;

        // Variables
        vm.model = {
          sessionUser: null,
          user: null,
          users: [],
          date: null,
          hours: 0,
          newSchedHours: 0,
          role: 'user',
          search: '',
          schedules: [],
          newSchedules: []
        }

        vm.view = {
          styles: ['pantallaUsuario', 'pantallaJefe'],
          style: null,
          styles2: ['', 'pantallaUsuarios', 'nuevoHorarioSemanal', 'nuevoHorarioEspecial'],
          style2: null,
          styles3: ['', 'pantallaMensaje'],
          style3: null,
          styles4: ['', 'procesando', 'procesado', 'errorDeSistema'],
          style4: null,
          days: ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'],
          schedStyles: ['principalSinDatos', 'principalConDatos', 'secundarioSinDatos', 'secundarioConDatos']
        }

        // Funciones
        vm.activate = activate;
        vm.initView = initView;
        vm.initModel = initModel;
        vm.initSchedules = initSchedules;

        vm.loadProfile = loadProfile;
        vm.loadUsers = loadUsers;
        vm.findUsersByOffices = findUsersByOffices;
        vm.displaySearch = displaySearch;
        vm.newWeeklySchedule = newWeeklySchedule;

        vm.getUserPhoto = getUserPhoto;
        vm.loadSchedules = loadSchedules;
        vm.setSchedules = setSchedules;
        vm.getSchedulesInDay = getSchedulesInDay;
        vm.getNewSchedulesInDay = getNewSchedulesInDay;
        vm.getDayName = getDayName;
        vm.selectUser = selectUser;

        vm.addSchedule = addSchedule;
        vm.removeSchedule = removeSchedule;
        vm.clearSchedule = clearSchedule;
        vm.updateNewHours = updateNewHours;
        vm.cancel = cancel;
        vm.saveScheduleWeek = saveScheduleWeek;

        // comunicacion con la directiva
        $scope.changeStart = changeStart;
        $scope.changeHours = changeHours;

        /////////////////////////////////////////
        activate();

        function activate() {
          vm.initView();
          vm.model.userId = '';
          Login.getSessionData()
            .then(function(s) {
                vm.model.sessionUser = s.user_id;
                vm.initModel();
            }, function(err) {
              console.log(err);
            });
        }

        function initView() {
          vm.view.style = vm.view.styles[0];
          vm.view.style2 = vm.view.styles2[0];
          vm.view.style3 = vm.view.styles3[0];
          vm.view.style4 = vm.view.styles4[0];
        }

        function initModel() {
          vm.model.users = [];
          vm.model.search = '';
          vm.model.role = 'user';
          vm.model.date = new Date();
          vm.loadProfile();
        }

        function displaySearch() {
          vm.view.style2 = (vm.view.style2 == vm.view.styles2[0]) ? vm.view.styles2[1] : vm.view.styles2[0];
        }

        function loadProfile() {
          Office.getOfficesByUserRole(vm.model.sessionUser, true, 'autoriza').then(function(ids) {
            vm.view.style = vm.view.styles[0];
            if (ids.length > 0) {
              vm.view.style = vm.view.styles[1];
              vm.findUsersByOffices(ids);
              vm.model.role = 'authority';
            } else {
              vm.loadUsers([vm.model.sessionUser]);
            }
          }, function(error) {
            console.log(error);
          });
        }

        function findUsersByOffices(ids) {
          Office.getOfficesUsers(ids).then(function (userIds) {
            vm.loadUsers(userIds);
          }, function(error) {
            console.log(error);
          });
        }

        function loadUsers(ids) {
          vm.model.users = [];
          if (ids.length <= 0) {
            return;
          }
          Users.findById(ids).then(function(users) {
            vm.model.users = (users == null) ? [] : users;
            for (var i = 0; i < users.length; i++) {
              var user = users[i];
              if (user.id == vm.model.sessionUser) {
                vm.model.user = user;
                break;
              }
            }
            vm.loadSchedules();
          }, function(error) {
            console.log('Error al buscar el usuario')
          });
        }

        function initSchedules() {
          vm.model.schedules = [[],[],[],[],[],[],[]];
          vm.model.hours = 0;
        }

        function getUserPhoto(user) {
          if (user == null || user.photo == null || user.photo == '') {
            return "../login/modules/img/imgUser.jpg";
          } else {
            return "/c/files.py?i=" + user.photo;
          }
        }

        function loadSchedules() {
          if (vm.model.user == null || vm.model.date == null) {
            return;
          }

          var uid = vm.model.user.id;
          vm.initSchedules();
          Assistance.getScheduleDataInWeek(uid, vm.model.date).then(function(data) {
            if (data == null || data.length <= 0) {
              return;
            }
            vm.setSchedules(data);
          }, function(error) {
            console.log('Error al buscar el usuario')
          });
        }

        function setSchedules(schedules) {
          for (var i = 0; i < schedules.length; i++) {
            var sch = schedules[i];
            sch.date = new Date(sch.date);
            vm.model.hours = vm.model.hours + sch.hours;
            var schs = [];
            for (var j = 0; j < sch.schedules.length; j++) {
              var start = new Date(sch.schedules[j].start);
              var end = new Date(sch.schedules[j].end);
              schs.push({start: start, end: end});
            }
            vm.model.schedules[sch.date.getDay()] = schs;
          }
        }

        function getSchedulesInDay(day) {
          return vm.model.schedules[day];
        }

        function getNewSchedulesInDay(day) {
          return (day == 7) ? vm.model.newSchedules[0] : vm.model.newSchedules[day];
        }

        function getDayName(index) {
          return (index == 7) ? vm.view.days[0] : vm.view.days[index];
        }

        function selectUser(user) {
          vm.view.style2 = vm.view.styles2[0];
          if (user == null) {
            return;
          }
          vm.model.user = user;
          vm.loadSchedules();
        }

        function newWeeklySchedule() {
          vm.view.style2 = vm.view.styles2[2];
          vm.model.newSchedules = [[],[],[],[],[],[],[]];
          vm.model.newSchedHours = vm.model.hours;
          for (var i = 0; i < vm.model.schedules.length; i++) {
            var sched = vm.model.schedules[i];
            var newSched = [];
            if (sched.length <= 0) {
              newSched.push({start: null, end: null, modified: false, hours: null, style: vm.view.schedStyles[0], day: i});
            } else {
              for (var j = 0; j < sched.length; j ++) {
                var start = sched[j].start;
                var end = sched[j].end;
                var hours = (end - start) / 60 / 60 / 1000;
                var style = (j == 0) ? vm.view.schedStyles[1] : vm.view.schedStyles[3];
                newSched.push({start: start, end: end, modified: false, hours: hours, style: style, day: i});
              }
            }
            vm.model.newSchedules[i] = newSched;
          }
        }

        function addSchedule(day) {
          vm.model.newSchedules[day].push({start: null, end: null, modified: true, hours: null, style: vm.view.schedStyles[2], day: day});
        }

        function removeSchedule(day, index) {
          var sched = vm.model.newSchedules[day];
          vm.model.newSchedHours = (sched[index].hours != null) ? vm.model.newSchedHours - sched[index].hours : vm.model.newSchedHours ;
          vm.model.newSchedules[day].splice(index, 1);
        }

        function clearSchedule(sch) {
          vm.model.newSchedHours = (sch.hours != null) ? vm.model.newSchedHours - sch.hours : vm.model.newSchedHours ;
          sch.start = null;
          sch.end = null;
          sch.hours = null;
          sch.modified = true;
          sch.operation = 'remove';
          var index = vm.view.schedStyles.indexOf(sch.style);
          sch.style = vm.view.schedStyles[index - 1];
        }

        function changeStart(newVal, oldVal, sched) {
          changeSchedule(newVal, oldVal, sched);
        }

        function changeHours(newVal, oldVal, sched) {
          var pattern = /^[0-9]+(.2|.25|.50|.5|.75|.7)?$/;
          if(!pattern.test(newVal)) {
            sched.hours = oldVal;
          }
          var patternAux = /^[0-9]+(.2|.7)+$/;
          if(patternAux.test(newVal)) {
            sched.hours = sched.hours + 0.05;
          }

          changeSchedule(newVal, oldVal, sched);
        }

        vm.validateHours = validateHours;
        function validateHours(sch) {
          var pattern = /^[0-9]+(.25|.50|.5|.75)?$/;
          if(!pattern.test(sch.hours)) {
            sch.hours = sch.oldHs;
          }
        }

        function changeSchedule(newVal, oldVal, sched) {
          if (oldVal == null && newVal != null) {
            var index = vm.view.schedStyles.indexOf(sched.style);
            sched.style = (index % 2 == 0) ? vm.view.schedStyles[index + 1] : sched.style;
          }
          if (!isValid(sched)) {
              return;
          }
          sched.modified = true;
          sched.operation = 'modify';
          vm.updateNewHours();
        }

        vm.getMinutes = getMinutes;
        function getMinutes() {
          return (vm.model.newSchedHours - vm.getHours()) * 60;
        }

        vm.getHours = getHours;
        function getHours() {
          return parseInt(vm.model.newSchedHours);
        }

        function updateNewHours() {
          var hours = 0;
          for (var i = 0; i < vm.model.newSchedules.length; i++) {
            var scheds = vm.model.newSchedules[i];
            for (var j = 0; j < scheds.length; j++) {
              hours = (scheds[j].hours != null) ? hours + scheds[j].hours : hours;
            }
          }
          vm.model.newSchedHours = hours;
        }

        function isValid(sched) {
          return (sched.hours != null && sched.hours > 0) && (sched.start != null)
        }

        function newSpecialSchedule() {
          vm.view.style2 = vm.view.styles2[3];
        }

        function cancel() {
          vm.view.style2 = vm.view.styles2[0];
        }

        function getSchedulesModifieds() {
          var modifiedScheds = [];
          for (var day = 0; day < 7 ; day++) {
            var newScheds = vm.model.newSchedules[day];
            var scheds = vm.model.schedules[day];
            var modified = false;

            if (scheds.length == 0 &&  isNull(newScheds)) {
              continue;
            }

            if (newScheds.length != scheds.length) {
              modified = true;
            } else {
              for (var i = 0; i < newScheds.length; i++) {
                var hours = (scheds[i].end - scheds[i].start) / 60 / 60 / 1000;
                if (newScheds[i].start != scheds[i].start || newScheds[i].hours != hours) {
                  modified = true;
                }
              }
            }
            if (modified) {
              modifiedScheds = modifiedScheds.concat(formatSchedules(newScheds));
            }
          }
          return modifiedScheds;
        }

        function formatSchedules(scheds) {
          var data = [];
          for (var i = 0; i < scheds.length; i++) {
            var s = {};
            s.weekday = (scheds[i].day == 0) ? 6 : scheds[i].day - 1;
            s.start = (scheds[i].start == null) ? 0 : (scheds[i].start.getHours() * 60 + scheds[i].start.getMinutes())
            var hours = (scheds[i].hours == null) ? 0 : scheds[i].hours;
            s.end = s.start + (parseInt(hours) * 60)  + ((hours * 60) % 60);
            data.push(s);
          }
          return data;
        }

        function saveScheduleWeek() {
          var scheds = getSchedulesModifieds();
          vm.view.style3 = vm.view.styles3[1];
          vm.view.style4 = vm.view.styles4[1];
          Assistance.createScheduleWeek(vm.model.user.id, vm.model.date, scheds).then(function(data) {

            $scope.$apply(function(){
              vm.view.style3 = vm.view.styles3[1];
              vm.view.style4 = vm.view.styles4[2];
            });
            $timeout(function() {
              $scope.$apply(function() {
                vm.loadSchedules();
                vm.view.style3 = vm.view.styles3[0];
                vm.view.style2 = vm.view.styles2[0];
              });
            }, 2500);

            console.log('ok');
          }, function(error) {
            $scope.$apply(function(){
              vm.view.style3 = vm.view.styles3[1];
              vm.view.style4 = vm.view.styles4[3];
            });
            $timeout(function() {
              $scope.$apply(function(){
                vm.view.style3 = vm.view.styles3[0];
                vm.view.style2 = vm.view.styles2[2];
              });
            }, 2500);
          });

        }

        function isNull(scheds) {
          if (scheds.length < 1) {
            return true;
          }

          if (scheds.length > 1) {
            return false;
          }

          return (scheds[0].start == null || scheds[0].hours == null);
        }


        ////////////////////////////////////////////////////
        $scope.$watch(function() {return vm.model.date;}, function(o,n) {
          if (vm.model.date == null) {
            vm.model.schedules = [];
            return;
          }
          vm.loadSchedules()
        });

    }
})();

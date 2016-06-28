(function() {
    'use strict';

    angular
        .module('mainApp')
        .controller('ScheduleController', ScheduleController);

    ScheduleController.$inject = ['$scope', 'Login', 'Users', 'Assistance', 'Office', '$filter'];

    /* @ngInject */
    function ScheduleController($scope, Login, Users, Assistance, Office, $filter) {
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
        vm.changeStart = changeStart;
        vm.changeHours = changeHours;

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
              newSched.push({start: null, end: null, modified: false, style: vm.view.schedStyles[0], day: i});
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
          vm.model.newSchedules[day].push({start: null, end: null, modified: true, style: vm.view.schedStyles[2], day: day});
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
          var index = vm.view.schedStyles.indexOf(sch.style);
          sch.style = vm.view.schedStyles[index - 1];
        }

        function changeStart(newVal, oldVal) {
          console.log("Viejo ctrl:" + oldVal);
          console.log("Nuevo ctrl:" + newVal);
        }

        $scope.changeSched = function(newVal, oldVal) {
          console.log("Viejo ctrl:" + oldVal);
          console.log("Nuevo ctrl:" + newVal);
        }

        function changeHours(event, schedule) {
          console.log(event)
        }

        function newSpecialSchedule() {
          vm.view.style2 = vm.view.styles2[3];
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

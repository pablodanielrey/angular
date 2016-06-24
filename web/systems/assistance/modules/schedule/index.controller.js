(function() {
    'use strict';

    angular
        .module('mainApp')
        .controller('ScheduleController', ScheduleController);

    ScheduleController.$inject = ['$scope', 'Login', 'Users', 'Assistance'];

    /* @ngInject */
    function ScheduleController($scope, Login, Users, Assistance) {
        var vm = this;

        // Variables
        vm.model = {
          sessionUser: null,
          user: null,
          date: null,
          hours: 0
        }

        vm.view = {
          styles: ['pantallaUsuario', 'pantallaJefe'],
          style: null,
          styles2: ['', 'pantallaUsuarios', 'nuevoHorarioSemanal', 'nuevoHorarioEspecial'],
          style2: null,
          styles3: ['', 'pantallaMensaje'],
          style3: null,
          styles4: ['', 'procesando', 'procesado', 'errorDeSistema'],
          style4: null
        }
        // Funciones
        vm.activate = activate;
        vm.initView = initView;
        vm.initModel = initModel;
        vm.initSchedules = initSchedules;

        vm.getUserPhoto = getUserPhoto;
        vm.loadSchedules = loadSchedules;
        vm.setSchedules = setSchedules;
        vm.getSchedulesInDay = getSchedulesInDay;


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
          loadUser(vm.model.sessionUser);
          vm.model.date = new Date();
        }

        function initSchedules() {
          vm.model.schedules = [[],[],[],[],[],[],[]];
          vm.model.hours = 0;
        }

        function loadUser(uid) {
          Users.findById([uid]).then(function(users) {
            vm.model.user = (users.length > 0) ? users[0] : null;
            vm.loadSchedules();
          }, function(error) {
            console.log('Error al buscar el usuario')
          });
        }

        function getUserPhoto() {
          if (vm.model.user == null || vm.model.user.photo == null || vm.model.user.photo == '') {
            return "../login/modules/img/imgUser.jpg";
          } else {
            return "/c/files.py?i=" + vm.model.user.photo;
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

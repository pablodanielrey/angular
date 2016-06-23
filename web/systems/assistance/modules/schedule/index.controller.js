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

          var start = new Date(vm.model.date);
          var day = start.getDay() - 1;
          var mondayDate = start.getDate() - (day < 0 ? 6 : day);
          start.setDate(mondayDate);
          var end = new Date(start);
          end.setDate(end.getDate() + 6);
          var uids = [vm.model.user.id];
          vm.initSchedules();
          Assistance.getScheduleData(uids, start, end).then(function(data) {
            if (data == null || data.length <= 0) {
              return;
            }
            vm.setSchedules(data[vm.model.user.id]);
          }, function(error) {
            console.log('Error al buscar el usuario')
          });
        }

        function setSchedules(schedules) {
          for (var i = 0; i < schedules.length; i++) {
            var sch = schedules[i];
            sch.start = new Date(sch.start);
            sch.end = new Date(sch.end);
            vm.model.hours = vm.model.hours + sch.hours;
            var elem = vm.model.schedules[sch.start.getDay()];
            elem.push(sch);
          }
          console.log(vm.model.schedules);
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

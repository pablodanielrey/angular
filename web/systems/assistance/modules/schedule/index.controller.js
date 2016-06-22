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
          userId: '',
          sessionUser: null,
          user: null,
          date: null
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

        vm.getUserPhoto = getUserPhoto;


        /////////////////////////////////////////
        activate();

        function activate() {
          vm.initView();
          vm.model.userId = '';
          Login.getSessionData()
            .then(function(s) {
                vm.model.userId = s.user_id;
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
          loadUser();
          vm.model.date = new Date();
        }

        function loadUser() {
          Users.findById([vm.model.userId]).then(function(users) {
            vm.model.user = (users.length > 0) ? users[0] : null;
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

    }
})();

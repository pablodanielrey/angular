(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('SchedulesCtrl', SchedulesCtrl);

    SchedulesCtrl.$inject = ['$scope', 'Assistance', 'Users', 'Login'];

    function SchedulesCtrl($scope, Assistance, Users, Login) {
        var vm = this;
        vm.model = {
          users: [],

          activate: false
        }

        vm.view = {
          style:'',
          profileAdmin: 'usuarioAdmin',
          profileUser: 'usuarioNormal',
          displayListUsers: 'pantallaUsuarios verHorario',
          displayPerson: 'pantallaEdicion verHorario',
          profile: 'user'
        }

        vm.selectUser = selectUser;


        $scope.$on('wamp.open', function(event, args) {
          activate();
        });

        activate();

        function activate() {
          if (vm.model.activate || Login.getPrivateTransport() == null) {
            return;
          }
          vm.model.activate = true;
          loadProfile();
          loadUsers();
        }

    /* **************************************************************************************************
                                        MANEJO DE PERFIL DE USUARIO
    * ************************************************************************************************ */

    function loadProfile() {
      // aca deberia hacer la llamada al servidor
      vm.view.profile = "admin";

      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      vm.view.style = style + ' ' + vm.view.displayListUsers;
    }

    /* **************************************************************************************************
                                        MANEJO DE PERSONAS
    * ************************************************************************************************ */

        function loadUsers() {
            vm.model.users = [];
            vm.model.users.push({dni: '31381082', name: 'Emanuel Joaquín', lastname: 'Pais', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
        }

        function selectUser(user) {
          var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
          vm.view.style = style + ' ' + vm.view.displayPerson;
        }



    }


})();

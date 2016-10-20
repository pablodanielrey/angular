(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('SchedulesCtrl', SchedulesCtrl);

    SchedulesCtrl.$inject = ['$scope', 'Assistance', 'Users'];

    function SchedulesCtrl($scope, Assistance, Users) {
        var vm = this;
        vm.model = {
          users: []
        }

        vm.view = {
          style:'',
          displayPerson: 'mostarPersona',
          displayHistory: 'mostrarHistorial',
          displayPersonAndHistory: 'mostrarPerson mostrarHistorial',
          displayError: 'mensaje error'
        }

        vm.selectUser = selectUser;
        activate();

        function activate() {
          vm.model.users = [];
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
          vm.model.users.push({dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});

        }

        function selectUser(user) {
          console.log(user);
          vm.view.style = vm.view.displayPersonAndHistory;
        }

    }


})();

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

        vm.selectUser = selectUser;
        activate();

        function activate() {
          vm.model.users = [];
          vm.model.users.push({name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarWoman.jpg'});
          vm.model.users.push({name: 'Emanuel Joaquín', lastname: 'Pais', img: 'img/avatarMan.jpg'});
          vm.model.users.push({name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarWoman.jpg'});
          vm.model.users.push({name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarWoman.jpg'});
          vm.model.users.push({name: 'Emanuel Joaquín', lastname: 'Pais', img: 'img/avatarMan.jpg'});
          vm.model.users.push({name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarWoman.jpg'});
          vm.model.users.push({name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarWoman.jpg'});
          vm.model.users.push({name: 'Emanuel Joaquín', lastname: 'Pais', img: 'img/avatarMan.jpg'});
          vm.model.users.push({name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarWoman.jpg'});
          vm.model.users.push({name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarWoman.jpg'});
          vm.model.users.push({name: 'Emanuel Joaquín', lastname: 'Pais', img: 'img/avatarMan.jpg'});
          vm.model.users.push({name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarWoman.jpg'});
          vm.model.users.push({name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarWoman.jpg'});
          vm.model.users.push({name: 'Emanuel Joaquín', lastname: 'Pais', img: 'img/avatarMan.jpg'});
          vm.model.users.push({name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarWoman.jpg'});
        }

        function selectUser(user) {
          console.log(user);
        }

    }


})();

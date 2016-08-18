(function() {
    'use strict';

    angular
        .module('issues')
        .controller('OrdersCreateCtrl', OrdersCreateCtrl);

    OrdersCreateCtrl.$inject = ['$scope', '$location', 'Login', 'Issues', 'Files'];

    /* @ngInject */
    function OrdersCreateCtrl($scope, $location,  Login, Issues, Files) {
        var vm = this;

        // variables del modelo
        vm.model = {
          user: {name: '-'},
          search: '',
          users: []
        }



        // variables de la vista
        vm.view = {
          searching: false
        }

        // métodos
        activate();
        vm.cancel = cancel;
        vm.searchUsers = searchUsers;
        vm.getUserPhoto = getUserPhoto;
        vm.selectUser = selectUser;


        function activate() {
          vm.model.userId = Login.getCredentials()['userId'];
        }

        function cancel() {
          $location.path('/orders');
        }

        function getUserPhoto(user) {
          if (user == null || user.photo == null) {
            return '/systems/login/modules/img/imgUser.jpg';
          } else {
            return Files.toDataUri(user.photo);
          }
        }

        function searchUsers() {
          if (vm.view.searching) {
            return
          }
          if (vm.model.search.length < 5) {
            vm.view.searching = false;
            return;
          }
          vm.view.searching = true;
          Issues.searchUsers(vm.model.search).then(
            function(users) {
              vm.view.searching = false;
              vm.model.users = users;
            }, function(error) {
              console.log(error);
            }
          );
        }

        function selectUser(user) {
          vm.view.style2 = '';
          vm.model.user = user;
        }

    }
})();

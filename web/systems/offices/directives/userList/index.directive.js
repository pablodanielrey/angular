(function() {
    'use strict';

    angular
        .module('offices')
        .directive('eUserList', eUserList);

    /* @ngInject */
    function eUserList() {
        var directive = {
            restrict: 'E',
            templateUrl: function(elem, attr) {
              var time = new Date().getTime();
              return 'directives/userList/index.html?t=' + time;
            },
            scope: {},
            link: linkFunc,
            controller: UserListCtrl,
            controllerAs: 'vm',
            bindToController: {
              users: '=users',
              deleteUser: '&removeUser',
              searchUsers: '&searchUsers'
            }
        };

        return directive;

        function linkFunc(scope, el, attr, ctrl) {

        }
    }

    UserListCtrl.$inject = ['$scope', 'Files'];

    /* @ngInject */
    function UserListCtrl($scope, Files) {
        var vm = this;

        vm.removeUser = removeUser;
        vm.search = search;
        vm.filter = '';
        vm.getUserPhoto = getUserPhoto;

        activate();

        function activate() {
          vm.filter = '';
        }

        function removeUser(user) {
          vm.deleteUser({user: user});
        }

        function search() {
          if (vm.filter.length < 5) {
            return;
          }
          vm.searchUsers({text:vm.filter});
        }

        function getUserPhoto(user) {
          if (user == null || user.photo == null) {
            var img = user != null && "genre" in user && user.genre != null && (user.genre.toLowerCase() == 'femenino' || user.genre.toLowerCase() == 'mujer') ? "img/avatarWoman.jpg" : "img/avatarMan.jpg";
            return img;
          } else {
            return Files.toDataUri(user.photo);
          }
        }

    }
})();

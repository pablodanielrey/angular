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

    UserListCtrl.$inject = ['$scope'];

    /* @ngInject */
    function UserListCtrl($scope) {
        var vm = this;

        vm.removeUser = removeUser;
        vm.search = search;
        vm.filter = '';

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
    }
})();

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
              deleteUser: '&removeUser'
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

        activate();

        function activate() {

        }

        function removeUser(user) {
          vm.deleteUser({user: user});
        }
    }
})();

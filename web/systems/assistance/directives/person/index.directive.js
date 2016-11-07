(function() {
    'use strict';

    angular
        .module('assistance')
        .directive('ePersonAssistance', ePersonAssistance);

    /* @ngInject */
    function ePersonAssistance() {
        var directive = {
            restrict: 'E',
            templateUrl: function(elem, attr) {
              var time = new Date().getTime();
              return 'directives/person/index.html?t=' + time;
            },
            scope: {},
            link: linkFunc,
            controller: PerrsonAssistanceController,
            controllerAs: 'vm',
            bindToController: {
              users: '=users',
              select: '&select'
            }
        };

        return directive;

        function linkFunc(scope, el, attr, ctrl) {

        }
    }

    PerrsonAssistanceController.$inject = ['$scope', '$timeout', 'Assistance', 'Users', '$window'];

    /* @ngInject */
    function PerrsonAssistanceController($scope, $timeout, Assistance, Users, $window) {
        var vm = this;
        vm.selectUser = selectUser;
        vm.searchUsers = searchUsers;
        vm.search = '';
        vm.searching = false;
        vm.aux = {
          searchTimer: null
        }

        activate();

        function activate() {
          var search = JSON.parse($window.sessionStorage.getItem('searchUser'));

          vm.search = '';
          vm.searching = false;
        }

        function selectUser(user) {
          vm.select({user:user})
        }

        function searchUsers() {
          if (vm.searching) {
            return
          }
          if (vm.search.length < 2) {
            vm.view.searching = false;
            return;
          }

          if (vm.aux.searchTimer != null) {
            $timeout.cancel(vm.aux.searchTimer);
            vm.aux.searchTimer = null;
          }

          vm.aux.searchTimer = $timeout(function() {
            vm.aux.searchTimer = null;
            vm.searching = true;
            Assistance.searchUsers(vm.search).then(Assistance.findUserByIds).then(Users.findPhotos).then(Users.photoToDataUri).then(
              function(users) {
                for (var i = 0; i< users.length; i++) {
                  users[i].photoSrc = (users[i].photoSrc.trim() == "" || !'photoSrc' in users[i]) ? 'img/avatarMan.jpg' : users[i].photoSrc
                }
                vm.searching = false;
                vm.users = users;
              }, function(error) {
                console.log(error);
              }
            );
          }, 1000);
        }
    }
})();

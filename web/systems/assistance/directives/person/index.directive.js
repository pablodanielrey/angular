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

    PerrsonAssistanceController.$inject = ['$scope'];

    /* @ngInject */
    function PerrsonAssistanceController($scope) {
        var vm = this;
        vm.selectUser = selectUser;
        vm.search = '';

        activate();

        function activate() {
          vm.search = '';
        }

        function selectUser(user) {
          vm.select({user:user})
        }
    }
})();

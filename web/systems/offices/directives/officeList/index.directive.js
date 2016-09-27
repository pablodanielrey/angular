(function() {
    'use strict';

    angular
        .module('offices')
        .directive('eOfficeList', eOfficeList);

    /* @ngInject */
    function eOfficeList() {
        var directive = {
            restrict: 'E',
            templateUrl: function(elem, attr) {
              var time = new Date().getTime();
              return 'directives/officeList/index.html?t=' + time;
            },
            scope: {},
            link: linkFunc,
            controller: OfficeListCtrl,
            controllerAs: 'vm',
            bindToController: {
              offices: '=offices',
              onRemove: '&onRemove',
              onCreate: '&onCreate'
            }
        };

        return directive;

        function linkFunc(scope, el, attr, ctrl) {

        }
    }

    OfficeListCtrl.$inject = ['$scope'];

    /* @ngInject */
    function OfficeListCtrl($scope) {
        var vm = this;
        vm.create = create;
        vm.remove = remove;

        activate();

        function activate() {

        }

        function create() {
          vm.onCreate();
        }

        function remove(office) {
          vm.onRemove({office: office});
        }
    }
})();

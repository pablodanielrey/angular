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
              return 'directives/officeList/index.html'
            },
            scope: {},
            link: linkFunc,
            controller: OfficeListCtrl,
            controllerAs: 'vm',
            bindToController: {

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

        activate();

        function activate() {

        }
    }
})();

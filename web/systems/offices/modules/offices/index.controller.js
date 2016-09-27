(function() {
    'use strict';

    angular
        .module('offices')
        .controller('OfficesCtrl', OfficesCtrl);

    OfficesCtrl.$inject = ['$scope'];

    /* @ngInject */
    function OfficesCtrl($scope) {
        var vm = this;

        activate();

        function activate() {

        }
    }
})();

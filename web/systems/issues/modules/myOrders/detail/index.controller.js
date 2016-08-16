(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersDetailCtrl', MyOrdersDetailCtrl);

    MyOrdersDetailCtrl.$inject = ['$scope', '$routeParams'];

    /* @ngInject */
    function MyOrdersDetailCtrl($scope, $routeParams) {
        var vm = this;

        activate();

        function activate() {
          console.log($routeParams);
        }
    }
})();

(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersCommentCtrl', MyOrdersCommentCtrl);

    MyOrdersCommentCtrl.$inject = ['$scope', '$routeParams'];

    /* @ngInject */
    function MyOrdersCommentCtrl($scope, $routeParams) {
        var vm = this;

        activate();

        function activate() {
          console.log($routeParams);
        }
    }
})();

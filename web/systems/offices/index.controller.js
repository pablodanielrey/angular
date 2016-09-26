(function() {
    'use strict'
    angular
      .module('offices')
      .controller('IndexCtrl', IndexCtrl);

    IndexCtrl.$inject = ['$scope'];

    function IndexCtrl($scope) {
        var vm = this;
        $scope.time = new Date().getTime();

    };

})();

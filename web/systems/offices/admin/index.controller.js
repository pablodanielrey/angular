(function() {
    'use strict'
    angular
      .module('offices.admin')
      .controller('IndexCtrl', IndexCtrl);

    IndexCtrl.$inject = ['$scope'];

    function IndexCtrl($scope) {
        $scope.time = new Date().getTime();

    };

})();

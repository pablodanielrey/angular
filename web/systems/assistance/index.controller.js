(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('IndexCtrl', IndexCtrl);

    IndexCtrl.$inject = ['$scope'];

    function IndexCtrl($scope) {
        var vm = this;
        $scope.time = new Date().getTime();

    };

})();

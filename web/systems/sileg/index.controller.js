(function() {
    'use strict'
    angular
      .module('sileg')
      .controller('IndexCtrl', IndexCtrl);

    IndexCtrl.$inject = ['$scope'];

    function IndexCtrl($scope) {
        var vm = this;
        $scope.nocache = new Date().getTime();

    };

})();

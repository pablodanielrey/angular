(function() {
    'use strict'
    angular
      .module('tutorias.coordinadores')
      .controller('IndexCtrl', IndexCtrl);

    IndexCtrl.$inject = ['$scope'];

    function IndexCtrl($scope) {
        $scope.time = new Date().getTime();

    };

})();

(function() {
    'use strict'
    angular
      .module('users.recover')
      .controller('IndexCtrl', IndexCtrl);

    IndexCtrl.$inject = ['$scope'];

    function IndexCtrl($scope) {
        $scope.time = new Date().getTime();

    };

})();

(function() {
    'use strict'
    angular
      .module('issues')
      .controller('IndexCtrl', IndexCtrl);

    IndexCtrl.$inject = ['$scope'];

    function IndexCtrl($scope) {
        var vm = this;
        $scope.time = new Date().getTime();
        $scope.getMenu = getMenu;
        $scope.getMenuCel = getMenuCel;

        function getMenu() {
          return 'modules/menu/index.html?t=' + $scope.time;
        }

        function getMenuCel() {
          return 'modules/menuCel/index.html?t=' + $scope.time;
        }
    };

})();

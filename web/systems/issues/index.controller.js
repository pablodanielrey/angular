(function() {
    'use strict'
    angular
      .module('issues')
      .controller('IndexCtrl', IndexCtrl);

    IndexCtrl.$inject = ['$scope'];

    function IndexCtrl($scope) {
        var vm = this;

        $scope.model = {
          hideMenu: false
        };

        $scope.t = (new Date()).getTime();

        $scope.hideMenu = function() {
          return $scope.model.hideMenu;
        }

        $scope.initialize = function() {
          $scope.styleMenu = 'full';
        }

        $scope.$on('$viewContentLoaded', function(event) {
          $scope.initialize();
        });
    };

})();

(function() {
    'use strict';

    angular
        .module('mainApp')
        .directive('schedDirective', schedDirective);

    /* @ngInject */
    function schedDirective() {
        var directive = {
            restrict: 'A',
            scope: false,
            replace: false,
            link: linkFunc
        };

        return directive;

        function linkFunc($scope, $el, $attr, ctrl) {
          $scope.$watch('sc.start',function(newVal,oldVal, obj) {
            if (newVal == oldVal) {
              return;
            }
            $scope.changeStart(newVal, oldVal, obj.sc);
          },true);
          $scope.$watch('sc.hours',function(newVal,oldVal, obj) {            
            obj.sc.oldHs = oldVal;
            if (newVal == undefined || newVal < 0) {
              return;
            }
            if (newVal == oldVal) {
              return;
            }
            $scope.changeHours(newVal, oldVal, obj.sc);
          },true);
        }
    }
})();

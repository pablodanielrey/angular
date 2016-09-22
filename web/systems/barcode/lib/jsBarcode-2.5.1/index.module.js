app.directive('barcode', function () {
  return {
      restrict: 'EA',
      scope: {data: '='},
      template: '<canvas id=barcode></canvas>',
      link: function($scope, element, attrs, ngModel){
          canvas = element.find('canvas')
          JsBarcode(canvas[0], $scope.data);
      }
  };
})

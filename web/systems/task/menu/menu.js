var app = angular.module('mainApp');

app.controller('MenuCtrl', ['$scope', function ($scope) {

  $scope.model = {
    class:'',
    items: [
      { name: 'Tareas',img:'fa fa-tag', url: '#/myTask' }
    ],
    cerrado : false
  };

  $scope.toggleMenu = function() {
    $scope.model.cerrado = !$scope.model.cerrado;
  };

}]);

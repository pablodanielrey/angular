var app = angular.module('mainApp');

app.controller('MenuCtrl', ['$scope', function ($scope) {

  $scope.model = {
    class:'',
    items: [
      { name: 'Crear Pedido',img:'fa fa-tag', url: '#/load' },
      { name: 'Pedidos',img:'fa fa-tags', url: '#/search' },
    ],
    cerrado : false
  };

  $scope.toggleMenu = function() {
    $scope.model.cerrado = !$scope.model.cerrado;
  };

}]);

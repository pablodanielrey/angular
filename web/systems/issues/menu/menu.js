var app = angular.module('mainApp');

app.controller('MenuCtrl', ['$scope', function ($scope) {

  $scope.model = {
    class:'',
    items: [
      { name: 'Pedidos',img:'fa fa-tag', url: '#/request' },
      { name: 'Administrar',img:'fa fa-tags', url: '#/manage' },
    ],
    cerrado : false
  };

  $scope.toggleMenu = function() {
    $scope.model.cerrado = !$scope.model.cerrado;
  };

}]);

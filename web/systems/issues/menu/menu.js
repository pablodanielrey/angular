var app = angular.module('mainApp');

app.controller('MenuCtrl', ['$scope', function ($scope) {

  $scope.model = {
    class:'',
    items: [
      { name: 'Crear Norma',img:'fa fa-file-text', url: '#/load' },
      { name: 'Buscar Norma',img:'fa fa fa-search', url: '#/search' },
    ],
    cerrado : false
  };

  $scope.toggleMenu = function() {
    $scope.model.cerrado = !$scope.model.cerrado;
  };

}]);

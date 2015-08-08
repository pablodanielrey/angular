var app = angular.module('mainApp');

app.controller('MenuCtrl', ["$rootScope", '$scope',

  function ($rootScope, $scope) {

    $scope.model = {
      class:'',
      items: [
        { name: 'Crear Norma', img:'fa fa-file-text', url: '#/load' },
        { name: 'Buscar Norma', img:'fa fa fa-search', url: '#/search' }
      ]
    }

    $scope.toggleMenu = function() {
      $scope.$parent.model.hideMenu = !$scope.$parent.model.hideMenu;
    }

  }
]);

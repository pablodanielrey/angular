angular
    .module('mainApp')
    .controller('MenuDigestoCtrl',MenuDigestoCtrl)

MenuDigestoCtrl.$inject = ['$scope','$rootScope'];

function MenuDigestoCtrl($scope,$rootScope) {

  $scope.model = {
    class:'',
    items: [
      { name: 'Crear Norma',img:'fa fa-file-text', url: '#/load' },
      { name: 'Buscar Norma',img:'fa fa fa-search', url: '#/search' },
    ],
    close : false
  }

  $scope.initialize = initialize;
  $scope.toggleMenu = toggleMenu;

  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  function initialize() {

  }

  function toggleMenu() {
    $scope.model.close = !$scope.model.close;
  }
}

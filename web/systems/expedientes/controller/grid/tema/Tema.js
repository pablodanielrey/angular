
/**
 * Controlador de la grilla de Tema
 */
app.controller("GridTemaCtrl", ["$scope", "$timeout", "Tema", "TableGrid", function ($scope, $timeout, Tema, TableGrid) {
 //***** codigo de inicializacion del controlador *****
  $timeout(function() {
    TableGrid.initialize($scope, Tema);
  },0);

  /***** escuchar evento de incializacion de "gridNumRows" *****/
  $scope.$on("gridNumRowsInitialized", function(event){
    TableGrid.changePagination($scope, Tema);
  });
  
  /**
   * Ir a pagina anterior
   */
  $scope.previousPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page-1, Tema);
  };
  
  /**
   * Ir a pagina siguiente
   */
  $scope.nextPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page+1, Tema);
  };
  
  /**
   * Ir a pagina determinada
   */
  $scope.goPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page, Tema);
  };
  
  /**
   * Cambiar tamanio de pagina
   */
  $scope.changePageSize = function(){
    TableGrid.changePagination($scope, Tema);
  };
  
  /** 
   * Buscar datos
   * @returns {undefined}
   */
  $scope.searchData = function(){
    TableGrid.searchData($scope, Tema);
  };
}]);

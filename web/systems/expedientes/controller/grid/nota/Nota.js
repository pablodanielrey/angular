
/**
 * Controlador de la grilla de Nota
 */
app.controller("GridNotaCtrl", ["$scope", "$timeout", "Nota", "TableGrid", function ($scope, $timeout, Nota, TableGrid) {
 //***** codigo de inicializacion del controlador *****
  $timeout(function() {
    TableGrid.initialize($scope, Nota);
  },0);

  /***** escuchar evento de incializacion de "gridNumRows" *****/
  $scope.$on("gridNumRowsInitialized", function(event){
    TableGrid.changePagination($scope, Nota);
  });
  
  /**
   * Ir a pagina anterior
   */
  $scope.previousPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page-1, Nota);
  };
  
  /**
   * Ir a pagina siguiente
   */
  $scope.nextPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page+1, Nota);
  };
  
  /**
   * Ir a pagina determinada
   */
  $scope.goPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page, Nota);
  };
  
  /**
   * Cambiar tamanio de pagina
   */
  $scope.changePageSize = function(){
    TableGrid.changePagination($scope, Nota);
  };
  
  /** 
   * Buscar datos
   * @returns {undefined}
   */
  $scope.searchData = function(){
    TableGrid.searchData($scope, Nota);
  };
}]);

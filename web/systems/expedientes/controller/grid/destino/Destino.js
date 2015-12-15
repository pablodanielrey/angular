
/**
 * Controlador de la grilla de Destino
 */
app.controller("GridDestinoCtrl", ["$scope", "$timeout", "Destino", "TableGrid", function ($scope, $timeout, Destino, TableGrid) {
 //***** codigo de inicializacion del controlador *****
  $timeout(function() {
    TableGrid.initialize($scope, Destino);
  },0);

  /***** escuchar evento de incializacion de "gridNumRows" *****/
  $scope.$on("gridNumRowsInitialized", function(event){
    TableGrid.changePagination($scope, Destino);
  });
  
  /**
   * Ir a pagina anterior
   */
  $scope.previousPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page-1, Destino);
  };
  
  /**
   * Ir a pagina siguiente
   */
  $scope.nextPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page+1, Destino);
  };
  
  /**
   * Ir a pagina determinada
   */
  $scope.goPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page, Destino);
  };
  
  /**
   * Cambiar tamanio de pagina
   */
  $scope.changePageSize = function(){
    TableGrid.changePagination($scope, Destino);
  };
  
  /** 
   * Buscar datos
   * @returns {undefined}
   */
  $scope.searchData = function(){
    TableGrid.searchData($scope, Destino);
  };
}]);

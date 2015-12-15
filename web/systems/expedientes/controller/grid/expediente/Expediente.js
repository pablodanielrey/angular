
/**
 * Controlador de la grilla de Expediente
 */
app.controller("GridExpedienteCtrl", ["$scope", "$timeout", "Expediente", "TableGrid", function ($scope, $timeout, Expediente, TableGrid) {
 //***** codigo de inicializacion del controlador *****
  $timeout(function() {
    TableGrid.initialize($scope, Expediente);
  },0);

  /***** escuchar evento de incializacion de "gridNumRows" *****/
  $scope.$on("gridNumRowsInitialized", function(event){
    TableGrid.changePagination($scope, Expediente);
  });
  
  /**
   * Ir a pagina anterior
   */
  $scope.previousPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page-1, Expediente);
  };
  
  /**
   * Ir a pagina siguiente
   */
  $scope.nextPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page+1, Expediente);
  };
  
  /**
   * Ir a pagina determinada
   */
  $scope.goPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page, Expediente);
  };
  
  /**
   * Cambiar tamanio de pagina
   */
  $scope.changePageSize = function(){
    TableGrid.changePagination($scope, Expediente);
  };
  
  /** 
   * Buscar datos
   * @returns {undefined}
   */
  $scope.searchData = function(){
    TableGrid.searchData($scope, Expediente);
  };
}]);

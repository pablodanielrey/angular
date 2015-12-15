
/**
 * Controlador de la grilla de Participacion
 */
app.controller("GridParticipacionCtrl", ["$scope", "$timeout", "Participacion", "TableGrid", function ($scope, $timeout, Participacion, TableGrid) {
 //***** codigo de inicializacion del controlador *****
  $timeout(function() {
    TableGrid.initialize($scope, Participacion);
  },0);

  /***** escuchar evento de incializacion de "gridNumRows" *****/
  $scope.$on("gridNumRowsInitialized", function(event){
    TableGrid.changePagination($scope, Participacion);
  });
  
  /**
   * Ir a pagina anterior
   */
  $scope.previousPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page-1, Participacion);
  };
  
  /**
   * Ir a pagina siguiente
   */
  $scope.nextPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page+1, Participacion);
  };
  
  /**
   * Ir a pagina determinada
   */
  $scope.goPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page, Participacion);
  };
  
  /**
   * Cambiar tamanio de pagina
   */
  $scope.changePageSize = function(){
    TableGrid.changePagination($scope, Participacion);
  };
  
  /** 
   * Buscar datos
   * @returns {undefined}
   */
  $scope.searchData = function(){
    TableGrid.searchData($scope, Participacion);
  };
}]);


/**
 * Controlador de la grilla de Persona
 */
app.controller("GridPersonaCtrl", ["$scope", "$timeout", "TableGrid", function ($scope, $timeout, TableGrid) {
 //***** codigo de inicializacion del controlador *****
  $timeout(function() {
    TableGrid.initialize($scope, "persona");
  },0);

  /***** escuchar evento de incializacion de "gridNumRows" *****/
  $scope.$on("gridNumRowsInitialized", function(event){
    TableGrid.changePagination($scope);
  });
  
  /**
   * Ir a pagina anterior
   */
  $scope.previousPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page-1);
  };
  
  /**
   * Ir a pagina siguiente
   */
  $scope.nextPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page+1);
  };
  
  /**
   * Ir a pagina determinada
   */
  $scope.goPage = function(){
    TableGrid.goPage($scope, $scope.pagination.page);
  };
  
  /**
   * Cambiar tamanio de pagina
   */
  $scope.changePageSize = function(){
    TableGrid.changePagination($scope);
  };
  
  /** 
   * Buscar datos
   * @returns {undefined}
   */
  $scope.searchData = function(){
    TableGrid.searchData($scope);
  };
  
  /**
   * Eliminar elemento de busqueda indice
   */
  $scope.deleteSearchIndex = function(index){
    $scope.search.index.splice(index, 1);
  };

  $scope.toggleSelection = function(id){
    TableGrid.toggleSelection($scope, id);
  };
  
  $scope.isSelected = function(id){
    return $scope.selection.indexOf(id) > -1;
  };

  $scope.toggleOrderBy = function(field){
    TableGrid.toggleOrderBy($scope, field);
  };
}]);

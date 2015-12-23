
/**
 * Controlador de la grilla de Archivo
 */
app.controller("GridCtrl", ["$scope", "$timeout", "Grid", function ($scope, $timeout, Grid) {
  
	/**
   * Inicializacion de fieldset: Se debe definir un identificador de fieldset
   * @param {midex} fieldsetId
   */
  $scope.init = function(label, title){
    Grid.initialize($scope, label, title);
  };

  /***** escuchar evento de incializacion de "gridNumRows" *****/
  $scope.$on("gridNumRowsInitialized", function(event){
    Grid.initializePagination($scope);
    Grid.getGridData($scope);
  });
  
  /***** modificar tamanio de pagina *****/
  $scope.changePageSize = function(){
    Grid.initializePagination($scope);
    Grid.getGridData($scope);
  };

  /**
   * Eliminar elemento de busqueda indice
   */
  $scope.deleteSearchIndex = function(index){
    $scope.search.index.splice(index, 1);
  };

  /** 
   * Ejecutar busqueda
   * @returns {undefined}
   */
  $scope.searchData = function(){
	$scope.pagination.disabled = true;
    Grid.getGridNumRows($scope);
  };

  $scope.previousPage = function(){
    Grid.goPage($scope, $scope.pagination.page-1);
  };
  
  $scope.nextPage = function(){
    Grid.goPage($scope, $scope.pagination.page+1);
  };
  
  $scope.goPage = function(){
    Grid.goPage($scope, $scope.pagination.page);
  };
  
  $scope.toggleSelection = function(id){
    Grid.toggleSelection($scope, id);
  };
  
  $scope.toggleOrderBy = function(field){
    Grid.toggleOrderBy($scope, field);
  };
  
  $scope.isSelected = function(id){
    return $scope.selection.indexOf(id) > -1;
  };
}]);

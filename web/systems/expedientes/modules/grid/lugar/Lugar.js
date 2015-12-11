
/**
 * Controlador de la grilla de Lugar
 */
app.controller("GridLugarCtrl", ["$scope", "$timeout", "Lugar", "TableGrid", function ($scope, $timeout, Lugar, TableGrid) {
 //***** codigo de inicializacion del controlador *****
  $timeout(function() {
    TableGrid.initialize($scope, Lugar);
  },0);

  /***** escuchar evento de incializacion de "gridNumRows" *****/
  $scope.$on("gridNumRowsInitialized", function(event){
    TableGrid.initializePagination($scope);
    TableGrid.getGridData($scope, Lugar);
  });
}]);

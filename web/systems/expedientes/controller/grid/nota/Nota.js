
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
    TableGrid.initializePagination($scope);
    TableGrid.getGridData($scope, Nota);
  });
}]);

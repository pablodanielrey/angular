
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
    TableGrid.initializePagination($scope);
    TableGrid.getGridData($scope, Destino);
  });
}]);

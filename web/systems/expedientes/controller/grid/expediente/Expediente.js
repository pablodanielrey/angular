
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
    TableGrid.initializePagination($scope);
    TableGrid.getGridData($scope, Expediente);
  });
}]);

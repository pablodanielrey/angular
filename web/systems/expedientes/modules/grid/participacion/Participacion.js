
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
    TableGrid.initializePagination($scope);
    TableGrid.getGridData($scope, Participacion);
  });
}]);

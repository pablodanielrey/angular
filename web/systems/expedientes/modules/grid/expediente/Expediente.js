
/**
 * Controlador de la grilla de Expediente
 */
app.controller("GridExpedienteCtrl", ["$scope", "$timeout", "Expediente", "TableGrid", function ($scope, $timeout, Expediente, TableGrid) {
 //***** codigo de inicializacion del controlador *****
  $timeout(function() {
    TableGrid.initialize($scope, Expediente);
  },0);

}]);

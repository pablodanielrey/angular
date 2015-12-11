
/**
 * Controlador de la grilla de Persona
 */
app.controller("GridPersonaCtrl", ["$scope", "$timeout", "Persona", "TableGrid", function ($scope, $timeout, Persona, TableGrid) {
 //***** codigo de inicializacion del controlador *****
  $timeout(function() {
    TableGrid.initialize($scope, Persona);
  },0);

}]);

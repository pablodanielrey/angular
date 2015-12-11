
/**
 * Controlador de la grilla de Tema
 */
app.controller("GridTemaCtrl", ["$scope", "$timeout", "Tema", "TableGrid", function ($scope, $timeout, Tema, TableGrid) {
 //***** codigo de inicializacion del controlador *****
  $timeout(function() {
    TableGrid.initialize($scope, Tema);
  },0);

}]);

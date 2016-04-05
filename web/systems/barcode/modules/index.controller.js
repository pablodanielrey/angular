
/**
 * Controlador principal, encargado de:
 *   Administracion de alerts
 *   Metodos de date picker
 */
app.controller("IndexCtrl", ["$scope", function ($scope) {
  
  $scope.documento = {
    id: 12345678,
    fecha: null,
    monto: null,
    curso: null,
    numero_documento: null
  }
 
  
  //***** definir titulo principal *****
  $scope.setMainTitle = function(mainTitle){ $scope.mainTitle = mainTitle; };

}]);



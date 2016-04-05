


//***** Controlador de formulario, encargado de administrar un conjunto de fieldsets *****
function DocumentoCtrl($scope, $window){
  
  $scope.submit = function(){ $window.location.href = "#barcode" }
  
  $scope.$on('$viewContentLoaded', function(event) { 
    $scope.documento.fecha = null;
    $scope.documento.monto = null;
    $scope.documento.curso = null;
    $scope.documento.numero_documento = null;
  });

}

app.controller("DocumentoCtrl", DocumentoCtrl);

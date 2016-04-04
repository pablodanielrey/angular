
app.config(['$routeProvider', function($routeProvider) {

  $routeProvider


  .when('/documento', { templateUrl: 'documento/Documento.html', controller:'DocumentoCtrl'})
  .when('/barcode', { templateUrl: 'documento/Barcode.html'  })         
  
  .otherwise({ redirectTo: '/barcode' });       
  
 
}]);

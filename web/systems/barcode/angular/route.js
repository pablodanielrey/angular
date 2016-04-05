
app.config(['$routeProvider', function($routeProvider) {

  $routeProvider


  .when('/documento', { templateUrl: 'modules/documento/Documento.html', controller:'DocumentoCtrl'})
  .when('/barcode', { templateUrl: 'modules/documento/Barcode.html'  })         
  
  .otherwise({ redirectTo: '/barcode' });       
  
 
}]);


var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/main', {
     templateUrl: '/systems/laboralInsertion/modules/main.html'
  })

  .when('/descargar', {
     templateUrl: '/systems/laboralInsertion/modules/download/download.html',
     controller: 'DownloadCtrl'
  })

  .when('/inscripcion', {
     templateUrl: '/systems/laboralInsertion/modules/inscription/inscription.html',
     controller: 'InscriptionCtrl'
  })

  .when('/busqueda', {
     templateUrl: '/systems/laboralInsertion/modules/search/search.html',
     controller: 'SearchCtrl'
  })

  .when('/envios', {
     templateUrl: '/systems/laboralInsertion/modules/send/send.html',
    //  controller: 'SendCtrl'
  })

  .when('/empresas', {
     templateUrl: '/systems/laboralInsertion/modules/company/company.html',
    //  controller: 'CompanyCtrl'
  })

  .when('/logout', {
     templateUrl: '/systems/login/modules/logout.html',
     controller: 'LogoutCtrl'
  })

  .otherwise({
    redirectTo: '/inscripcion'
  });

}]);

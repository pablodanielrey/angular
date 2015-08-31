
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
     controller: 'EditInsertionDataCtrl'
  })

  .otherwise({
    redirectTo: '/main'
  });

}]);


var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/main', {
     templateUrl: '/systems/laboralInsertion/modules/main.html'
  })

  .when('/download', {
     templateUrl: '/systems/laboralInsertion/modules/download/download.html',
     controller: 'DownloadCtrl'
  })

  .otherwise({
    redirectTo: '/main'
  });

}]);

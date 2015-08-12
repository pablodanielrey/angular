
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

  .when('/upload', {
     templateUrl: '/systems/laboralInsertion/modules/upload/editData.html',
     controller: 'EditInsertionDataCtrl'
  })

  .otherwise({
    redirectTo: '/main'
  });

}]);

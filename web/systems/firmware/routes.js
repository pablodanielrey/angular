var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/firmware/', {
    templateUrl: '/modules/systems/firmware/enroll.html',
    controller: 'EnrollCtrl'
  })

  .otherwise({
      redirectTo: '/error'
  });

  }
])

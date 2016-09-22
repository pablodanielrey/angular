
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/confirmAccountRequest/:hash?', {
    templateUrl: '/modules/account/confirmAccountRequest.html',
    controller: 'ConfirmAccountRequestCtrl'
  })

  .otherwise({
      redirectTo: '/error'
  });

  }
])

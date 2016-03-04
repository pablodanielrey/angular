
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/confirmMail/:hash', {
    templateUrl: '/modules/users/confirmMail.html',
    controller: 'ConfirmMailCtrl'
  })

  .otherwise({
      redirectTo: '/error'
  });

  }
])

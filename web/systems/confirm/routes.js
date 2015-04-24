
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/confirmMail/:hash', {
    templateUrl: '/modules/users/confirmMail.html',
    controller: 'ConfirmMailCtrl'
  })

  .when('/confirmAccountRequest/:hash?', {
    templateUrl: '/modules/account/confirmAccountRequest.html',
    controller: 'ConfirmAccountRequestCtrl'
  })

  .otherwise({
      redirectTo: '/main'
  });  

  }
])

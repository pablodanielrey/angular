
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

    .when('/changePassword/:username?/:hash?', {
      templateUrl: '/systems/pass/modules/change/changePassword.html',
      controller: 'ChangePasswordCtrl'
    })

    .when('/cp', {
      templateUrl: '/systems/pass/modules/change/changePassword.html',
      controller: 'ChangePasswordCtrl'
    })

    .otherwise({
        redirectTo: '/cp'
    });
  }
])

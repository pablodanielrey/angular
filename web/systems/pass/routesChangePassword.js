
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

    .when('/changePassword/:username?/:hash?', {
      templateUrl: '/modules/account/changePassword.html',
      controller: 'ChangePasswordCtrl'
    })

    .otherwise({
        redirectTo: '/main'
    });
  }
])

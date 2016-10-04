
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/createAccounts', {
     templateUrl: '/systems/account/modules/createAccounts/index.html',
     controller: 'CreateAccountsCtrl'
  })

  .when('/editAccounts', {
     templateUrl: '/systems/account/modules/editAccounts/index.html',
     controller: 'EditAccountsCtrl'
  })


  .when('/logout', {
     templateUrl: '/systems/login/modules/logout.html',
     controller: 'LogoutCtrl'
  })

  .otherwise({
    redirectTo: '/editAccounts'
  });

}]);

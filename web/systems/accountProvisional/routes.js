
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/home', {
     templateUrl: '/systems/accountProvisional/modules/home/index.html',
     controller: 'HomeCtrl'
  })

  .when('/request', {
     templateUrl: '/systems/accountProvisional/modules/request/index.html',
     controller: 'RequestCtrl'
  })


  .when('/logout', {
     templateUrl: '/systems/login/modules/logout.html',
     controller: 'LogoutCtrl'
  })

  .otherwise({
    redirectTo: '/home'
  });

}]);

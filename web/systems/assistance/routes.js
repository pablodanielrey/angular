
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/home', {
     templateUrl: '/systems/assistance/modules/home/index.html',
     controller: 'HomeCtrl'
  })

  .when('/request', {
     templateUrl: '/systems/assistance/modules/request/index.html',
     controller: 'RequestCtrl'
  })

  .when('/schedule', {
     templateUrl: '/systems/assistance/modules/schedule/index.html',
     controller: 'ScheduleController',
     controllerAs: 'vm'
  })



  .when('/logout', {
     templateUrl: '/systems/login/modules/logout.html',
     controller: 'LogoutCtrl'
  })

  .otherwise({
    redirectTo: '/home'
  });

}]);

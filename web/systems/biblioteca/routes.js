
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/library', {
     templateUrl: '/systems/biblioteca/modules/library/index.html',
     controller: 'LibraryCtrl'
  })

  .when('/logout', {
     templateUrl: '/systems/login/modules/logout.html',
     controller: 'LogoutCtrl'
  })

  .otherwise({
    redirectTo: '/library'
  });

}]);

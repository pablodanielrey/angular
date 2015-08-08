
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/main', {
     templateUrl: '/systems/fce/modules/home/home.html'
  })

  .when('/logout', {
     templateUrl: '/systems/login/modules/logout.html',
     controller: 'LogoutCtrl'
  })

  .otherwise({
    redirectTo: '/main'
  });

}]);

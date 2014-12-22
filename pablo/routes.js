 
var app = angular.module('mainApp')

app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider
      .when('/main', {
	    templateUrl: 'views/main.html',
	    controller: 'MainCtrl'
      })
      .when('/test', {
	    templateUrl: 'views/test.html',
	    controller: 'TestCtrl'
      })
      .otherwise({
 	redirectTo: '/main'
      });
  }
])
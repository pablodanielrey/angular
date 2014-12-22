 
var app = angular.module('mainApp')

app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider
      .when('/main', {
	    templateUrl: 'views/main.html',
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

var app = angular.module('mainApp')

app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider

      .when('/main', {
	       templateUrl: 'views/main.html',
         controller: 'MainCtrl'
      })

      .when('/login', {
	       templateUrl: 'views/login.html',
         controller: 'LoginCtrl'
      })

	    .when('/logout', {
	       templateUrl: 'views/logout.html',
         controller: 'LogoutCtrl'
      })

      .when('/menu', {
        templateUrl: 'views/menu.html',
      })

	  .when('/createAccountRequest', {
	    templateUrl: 'views/createAccountRequest.html',
      })
	  .when('/confirmAccountRequest', {
	    templateUrl: 'views/confirmAccountRequest.html',
      })
	  .when('/editUsers', {
	    templateUrl: 'views/editUsers.html',
      })
	  .when('/editProfile', {
	    templateUrl: 'views/editProfile.html',
      })
	  .when('/resetPassword', {
	    templateUrl: 'views/resetPassword.html',
      })
	  .when('/changePassword', {
	    templateUrl: 'views/changePassword.html',
      })
	  .when('/editGroups', {
	    templateUrl: 'views/editGroups.html',
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

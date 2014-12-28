
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

    $routeProvider

      .when('/main', {
	       templateUrl: 'views/main.html',
         controller: 'MainCtrl'
      })

      .when('/login', {
	       templateUrl: 'modules/login/login.html',
         controller: 'LoginCtrl'
      })

	    .when('/logout', {
	       templateUrl: 'modules/login/logout.html',
         controller: 'LogoutCtrl'
      })

      .when('/createAccountRequest', {
        templateUrl: 'modules/account/createAccountRequest.html',
        controller: 'CreateAccountRequestCtrl'
      })

      .when('/listAccountRequests', {
        templateUrl: 'modules/account/listAccountRequests.html',
        controller: 'ListAccountRequestsCtrl'
      })

      .when('/resetPassword', {
        templateUrl: 'views/resetPassword.html',
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

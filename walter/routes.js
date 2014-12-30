
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

      .when('/listUsers', {
        templateUrl: 'modules/users/listUsers.html',
        controller: 'ListUsersCtrl'
      })

      .when('/editProfile', {
        templateUrl: 'modules/users/editProfile.html',
        controller: 'EditProfileCtrl'
      })

      .when('/editUsers', {
        templateUrl: 'modules/users/editUsers.html',
        controller: 'EditUsersCtrl'
      })

      .otherwise({
 	      redirectTo: '/main'
      });
  }
])

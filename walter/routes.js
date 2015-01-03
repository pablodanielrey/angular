
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

    $routeProvider

      .when('/main', {
	       templateUrl: 'views/main.html',
         controller: 'MainCtrl'
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

      .when('/status', {
        templateUrl: 'modules/admin/status.html',
        controller: 'StatusCtrl'
      })

      .when('/confirmMail:hash', {
        templateUrl: 'modules/users/confirmMail.html',
        controller: 'ConfirmMailCtrl'
      })


      .otherwise({
 	      redirectTo: '/main'
      });
  }
])

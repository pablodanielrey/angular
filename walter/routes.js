
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

    $routeProvider

      .when('/main', {
	       templateUrl: '/views/main.html',
         controller: 'MainCtrl'
      })

	    .when('/logout', {
	       templateUrl: '/modules/login/logout.html',
         controller: 'LogoutCtrl'
      })

      .when('/createAccountRequest', {
        templateUrl: '/modules/account/createAccountRequest.html',
        controller: 'CreateAccountRequestCtrl'
      })

      .when('/listAccountRequests', {
        templateUrl: '/modules/account/accountRequestsIndex.html',

      })

      .when('/listUsers', {
        templateUrl: '/modules/users/listUsers.html',
        controller: 'ListUsersCtrl'
      })

      .when('/editProfile', {
        templateUrl: '/modules/users/editProfile.html',
        controller: 'EditProfileCtrl'
      })

      .when('/editUsers', {
        templateUrl: '/modules/users/editUsers.html',
        controller: 'EditUsersCtrl'
      })

      .when('/status', {
        templateUrl: '/modules/admin/status.html',
        controller: 'StatusCtrl'
      })

      .when('/confirmMail/:hash', {
        templateUrl: '/modules/users/confirmMail.html',
        controller: 'ConfirmMailCtrl'
      })

      .when('/confirmAccountRequest/:hash?', {
        templateUrl: '/modules/account/confirmAccountRequest.html',
        controller: 'ConfirmAccountRequestCtrl'
      })

      .when('/changePassword/:username?/:hash?', {
        templateUrl: '/modules/account/changePassword.html',
        controller: 'ChangePasswordCtrl'
      })

      .when('/resetPassword', {
        templateUrl: '/modules/account/resetPassword.html',
        controller: 'ResetPasswordCtrl'
      })

      .when('/editUserProfile', {
        templateUrl: '/modules/users/editUserProfile.html',
        controller: 'EditUserProfileCtrl'
      })


      .when('/editGroups', {
        templateUrl: '/modules/groups/editGroups.html',
        controller: 'EditGroupsCtrl'
      })

      .when('/editStudent', {
        templateUrl: '/modules/systems/student/editStudent.html',
        controller: 'EditStudentCtrl'
      })


      .when('/editInsertion', {
        templateUrl: '/modules/systems/insercion/editData.html',
        controller: 'EditInsertionDataCtrl'
      })

      .when('/acceptTermsAndConditionsInsertion', {
        templateUrl: '/modules/systems/insercion/termsAndConditions.html',
        controller: 'LaboralInsertionTermsAndConditionsCtrl'
      })


	.when('/editAccountRequest', {
		templateUrl: '/modules/account/accountRequestEdit.html',
		controller: 'AccountRequestEditCtrl'
	})

	.when('/au24', {
		templateUrl: '/modules/systems/au24/au24.html',
		controller: 'Au24Ctrl'
	})

      .otherwise({
 	      redirectTo: '/main'
      });
  }
])

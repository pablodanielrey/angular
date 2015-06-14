
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

  .when('/mainAssistance', {
    templateUrl: '/modules/systems/assistance/assistance.html',
    controller: 'AssistanceCtrl'
  })

  .when('/acceptTermsAndConditionsInsertion', {
    templateUrl: '/modules/systems/insercion/termsAndConditions.html',
    controller: 'LaboralInsertionTermsAndConditionsCtrl'
  })

  .when('/editSystems', {
    templateUrl: '/modules/systems/editSystems.html',
    controller: 'EditSystemsCtrl'
  })

  .when('/summaryAssistance', {
      templateUrl: '/modules/systems/assistance/assistance.html',
      controller: 'AssistanceCtrl'
  })

  .when('/assistanceFails', {
      templateUrl: '/modules/systems/assistance/fails.html',
      controller: 'AssistanceFailsCtrl'
  })

  .when('/assistanceFailsFilters', {
      templateUrl: '/modules/systems/assistance/failsFilters.html',
      controller: 'AssistanceFailsFiltersCtrl'
  })

  .when('/requestAssistance', {
      templateUrl: '/modules/systems/assistance/requestAssistance.html',
      controller: 'RequestAssistanceCtrl'
  })

  .when('/adminRequestAssistance', {
      templateUrl: '/modules/systems/assistance/adminRequestAssistance.html',
      controller: 'AdminRequestAssistanceCtrl'
  })

  .when('/medicalLicenses', {
      templateUrl: '/modules/systems/assistance/medicalLicenses.html',
      controller: 'MedicalLicensesCtrl'
  })
  .when('/requestAuthority', {
      templateUrl: '/modules/systems/assistance/requestAuthority.html',
      controller: 'RequestAuthorityCtrl'
  })

  .when('/adminRequestOverTime', {
      templateUrl: '/modules/systems/assistance/adminRequestOverTime.html',
      controller: 'AdminRequestOverTimeCtrl'
  })

  .when('/showAssistance', {
      templateUrl: '/modules/systems/assistance/showAssistance.html',
      controller: 'ShowAssistanceCtrl'
  })
  .when('/mySchedule', {
      templateUrl: '/modules/systems/assistance/mySchedule.html',
      controller: 'MyScheduleCtrl'
  })



	.when('/editAccountRequest', {
		templateUrl: '/modules/account/accountRequestEdit.html',
		controller: 'AccountRequestEditCtrl'
	})

	.when('/au24', {
		templateUrl: '/modules/systems/au24/au24.html',
		controller: 'Au24Ctrl'
	})


	.when('/test', {
		templateUrl: '/modules/test/test.html',
		controller: 'TestCtrl'
	})

  .when('/tutors', {
    templateUrl: '/modules/systems/tutors/tutors.html',
    controller: 'TutorsCtrl'
  })

  .when('/userAssistanceManagement', {
      templateUrl: '/modules/systems/assistance/usersAssistanceManagement/index.html',
      controller: 'UsersAssistanceManagementCtrl'
  })

  .when('/requestGeneralJustifications', {
      templateUrl: '/modules/systems/assistance/requestGeneralJustifications/index.html',
      controller: 'RequestGeneralJustificationsCtrl'
  })

  .when('/usersAssistanceManagementMediator', {
    templateUrl: '/modules/systems/assistance/usersAssistanceManagementMediator/index.html',
    controller: 'UsersAssistanceManagementMediatorCtrl'
  })

  .otherwise({
    redirectTo: '/main'
  });

}]);

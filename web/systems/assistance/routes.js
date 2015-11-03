
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/logout', {
     templateUrl: '/systems/login/modules/logout.html',
     controller: 'LogoutCtrl'
  })

  .when('/main', {
    templateUrl: '/systems/assistance/modules/assistance.html',
    controller: 'AssistanceCtrl'
  })

  .when('/summaryAssistance', {
      templateUrl: '/systems/assistance/modules/assistance.html',
      controller: 'AssistanceCtrl'
  })

  .when('/assistanceFails', {
      templateUrl: '/systems/assistance/modules/fails/fails.html',
      controller: 'AssistanceFailsCtrl'
  })

  .when('/assistanceFailsFilters', {
      templateUrl: '/systems/assistance/modules/failsFilters.html',
      controller: 'AssistanceFailsFiltersCtrl',
      controllerAs: 'vm'
  })



  .when('/requestAssistance', {
      templateUrl: '/systems/assistance/modules/requestJustifications/index.html',
      controller: 'RequestJustificationsCtrl'
  })


  .when('/adminRequestAssistance', {
      templateUrl: '/systems/assistance/modules/adminRequest/adminRequestAssistance.html',
      controller: 'AdminRequestAssistanceCtrl'
  })

  .when('/medicalLicenses', {
      templateUrl: '/systems/assistance/modules/medicalLicenses.html',
      controller: 'MedicalLicensesCtrl'
  })
  .when('/requestAuthority', {
      templateUrl: '/systems/assistance/modules/overtime/requestAuthority.html',
      controller: 'RequestAuthorityCtrl'
  })

  .when('/adminRequestOverTime', {
      templateUrl: '/systems/assistance/modules/overtime/adminRequestOverTime.html',
      controller: 'AdminRequestOverTimeCtrl'
  })

  .when('/showAssistance', {
      templateUrl: '/systems/assistance/modules/workedHours/showAssistance.html',
      controller: 'ShowAssistanceCtrl'
  })
  .when('/mySchedule', {
      templateUrl: '/systems/assistance/modules/workedHours/mySchedule.html',
      controller: 'MyScheduleCtrl'
  })

	.when('/editAccountRequest', {
		templateUrl: '/modules/account/accountRequestEdit.html',
		controller: 'AccountRequestEditCtrl'
	})

  .when('/userAssistanceManagement', {
      templateUrl: '/systems/assistance/modules/usersAssistanceManagement/index.html',
      controller: 'UsersAssistanceManagementCtrl'
  })

  .when('/requestGeneralJustifications', {
      templateUrl: '/systems/assistance/modules/requestGeneralJustifications/index.html',
      controller: 'RequestGeneralJustificationsCtrl'
  })

  .when('/usersAssistanceManagementMediator', {
    templateUrl: '/systems/assistance/modules/usersAssistanceManagementMediator/index.html',
    controller: 'UsersAssistanceManagementMediatorCtrl'
  })

  .when('/manageJustificationsStock', {
    templateUrl: '/systems/assistance/modules/manageJustificationsStock/index.html',
    controller: 'ManageJustificationsStockCtrl'
  })

  .when('/managePositions', {
    templateUrl: '/systems/assistance/modules/managePositions/index.html',
    controller: 'ManagePositionsCtrl'
  })

  .otherwise({
    redirectTo: '/main'
  });

}]);

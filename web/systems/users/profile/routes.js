(function() {
    'use strict'
    var app = angular.module('users.profile')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/adminUser', {templateUrl: 'modules/adminUser/index.html', controller: 'AdminUserCtrl'})
      .when('/changePasswordSendCode', {templateUrl: 'modules/changePasswordSendCode/index.html', controller: 'ChangePasswordSendCodeCtrl'})
      .when('/changePasswordSetCode', {templateUrl: 'modules/changePasswordSetCode/index.html', controller: 'ChangePasswordSetCodeCtrl'})
      .when('/changePassword', {templateUrl: 'modules/changePassword/index.html', controller: 'ChangePasswordCtrl'})
      .when('/listEmails', {templateUrl: 'modules/listEmails/index.html', controller: 'ListEmailsCtrl'})

      .otherwise({
        redirectTo: '/adminUser'
      });

    }]);

})();

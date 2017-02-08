(function() {
    'use strict'
    var app = angular.module('users.profile')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/adminUser', {templateUrl: 'modules/adminUser/index.html', controller: 'AdminUserCtrl'})
      .when('/sendCode', {templateUrl: 'modules/sendCode/index.html', controller: 'SendCodeCtrl'})
      .when('/setCode', {templateUrl: 'modules/setCode/index.html', controller: 'SetCodeCtrl'})
      .when('/changePassword', {templateUrl: 'modules/changePassword/index.html', controller: 'ChangePasswordCtrl'})
      .when('/listEmails', {templateUrl: 'modules/listEmails/index.html', controller: 'ListEmailsCtrl'})

      .otherwise({
        redirectTo: '/adminUser'
      });

    }]);

})();

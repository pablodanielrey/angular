(function() {
    'use strict'
    var app = angular.module('users.recover')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/identificate', {templateUrl: 'modules/identificate/index.html', controller: 'IdentificateCtrl'})
      .when('/changePasswordSetCode', {templateUrl: 'modules/changePasswordSetCode/index.html', controller: 'ChangePasswordSetCodeCtrl'})
      .when('/changePassword', {templateUrl: 'modules/changePassword/index.html', controller: 'ChangePasswordCtrl'})



      .otherwise({
        redirectTo: '/identificate'
      });

    }]);

})();

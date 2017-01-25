(function() {
    'use strict'
    var app = angular.module('users')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/adminUser', {templateUrl: 'modules/adminUser/index.html', controller: 'AdminUserCtrl'})
      .when('/changePassword', {templateUrl: 'modules/changePassword/index.html', controller: 'ChangePasswordCtrl'})

      .otherwise({
        redirectTo: '/adminUser'
      });

    }]);

})();

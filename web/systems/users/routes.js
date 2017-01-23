(function() {
    'use strict'
    var app = angular.module('users')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/listUsers', {templateUrl: 'modules/listUsers/index.html', controller: 'ListUsersCtrl'})
      .when('/adminUser', {templateUrl: 'modules/adminUser/index.html', controller: 'AdminUserCtrl'})

      .otherwise({
        redirectTo: '/listUsers'
      });

    }]);

})();

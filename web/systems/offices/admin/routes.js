(function() {
    'use strict'
    var app = angular.module('offices.admin')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/adminOffice', {templateUrl: 'modules/adminOffice/index.html', controller: 'AdminOfficeCtrl'})

      .when('/listOffices', {templateUrl: 'modules/listOffices/index.html', controller: 'ListOfficesCtrl'})
      .when('/listOfficesByUser', {templateUrl: 'modules/listOfficesByUser/index.html', controller: 'ListOfficesByUserCtrl'})

      .when('/listUsersByOffice', {templateUrl: 'modules/listUsersByOffice/index.html', controller: 'ListUsersByOfficeCtrl'})
      .when('/listUsers', {templateUrl: 'modules/listUsers/index.html', controller: 'ListUsersCtrl'})

      .otherwise({
        redirectTo: '/listOffices'
      });

    }]);

})();

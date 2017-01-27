(function() {
    'use strict'
    var app = angular.module('offices.admin')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/listOffices', {templateUrl: 'modules/listOffices/index.html', controller: 'ListOfficesCtrl'})
      .when('/adminOffice', {templateUrl: 'modules/adminOffice/index.html', controller: 'AdminOfficeCtrl'})

      .otherwise({
        redirectTo: '/listOffices'
      });

    }]);

})();

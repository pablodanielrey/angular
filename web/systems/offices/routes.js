(function() {
    'use strict'
    var app = angular.module('offices')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/create', {
         templateUrl: 'modules/offices/index.html',
         controller: 'OfficesCtrl',
         controllerAs: 'vm'
      })

      .when('/edit/:officeId', {
         templateUrl: 'modules/offices/index.html',
         controller: 'OfficesCtrl',
         controllerAs: 'vm'
      })

      .when('/list', {
         templateUrl: 'modules/offices/index.html',
         controller: 'OfficesCtrl',
         controllerAs: 'vm'
      })

      .otherwise({
        redirectTo: '/list'
      });

    }]);

})();

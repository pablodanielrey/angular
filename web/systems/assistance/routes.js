(function() {
    'use strict'
    var app = angular.module('assistance')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/logs', {
         templateUrl: 'modules/logs/index.html',
         controller: 'LogsCtrl',
         controllerAs: 'vm'
      })
      .when('/reports', {
         templateUrl: 'modules/reports/index.html',
         controller: 'ReportsCtrl',
         controllerAs: 'vm'
      })
      // tengo que poner los dos para que tome el /schedules, por angular
      .when('/schedules', {
         templateUrl: 'modules/schedules/schedules.html',
         controller: 'SchedulesCtrl',
         controllerAs: 'vm'
      })
      .when('/schedules/:personId', {
         templateUrl: 'modules/schedules/schedules.html',
         controller: 'SchedulesCtrl',
         controllerAs: 'vm'
      })

      .otherwise({
        redirectTo: '/logs'
      });

    }]);

})();

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

      // edicion de horario semanal
      .when('/weekSchedules/:personId', {
         templateUrl: 'modules/schedules/editWeeklySchedule/index.html',
         controller: 'EditWeeklySchCtrl',
         controllerAs: 'vm'
      })

      // edicion de horario semanal
      .when('/hoursSchedules/:personId', {
         templateUrl: 'modules/schedules/editHoursSchedule/index.html',
         controller: 'EditHoursSchCtrl',
         controllerAs: 'vm'
      })

      // edicion de horario especial
      .when('/specialSchedules/:personId', {
         templateUrl: 'modules/schedules/editSpecialSchedule/index.html',
         controller: 'EditSpecialSchCtrl',
         controllerAs: 'vm'
      })

      .otherwise({
        redirectTo: '/logs'
      });

    }]);

})();

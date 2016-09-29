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

      .otherwise({
        redirectTo: '/logs'
      });

    }]);

})();

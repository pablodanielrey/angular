(function() {
    'use strict'
    var app = angular.module('sileg')

    app.config(['$routeProvider', function($routeProvider) {
      
      $routeProvider

      .when('/staff', {templateUrl: 'modules/staff/staff.html', controller: 'StaffCtrl', controllerAs: 'vm' })
      .otherwise({ redirectTo: '/staff' });

    }]);

})();

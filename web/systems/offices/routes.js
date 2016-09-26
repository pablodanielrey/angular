(function() {
    'use strict'
    var app = angular.module('offices')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .otherwise({
        redirectTo: '/home',
        templateUrl: 'modules/listOffices/index.html'
      });

    }]);

})();

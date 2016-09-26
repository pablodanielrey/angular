(function() {
    'use strict'
    var app = angular.module('issues')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/main', {
         templateUrl: 'modules/home/index.html',
         controller: 'HomeCtrl'
      })

      .otherwise({
        redirectTo: '/home',
        templateUrl: 'modules/home/index.html'
      });

    }]);

})();

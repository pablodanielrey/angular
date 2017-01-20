(function() {
    'use strict'
    var app = angular.module('users')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider



      .when('/listUsers', {
         templateUrl: 'modules/listUsers/index.html',
         controller: 'ListUsersCtrl',

      })



      .otherwise({
        redirectTo: '/listUsers'
      });

    }]);

})();

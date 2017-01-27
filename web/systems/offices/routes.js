(function() {
    'use strict'
    var app = angular.module('users')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/listUsers', {
         templateUrl: 'modules/users/listUsers.html',
         controller: 'ListUsersCtrl',
         controllerAs: 'vm'
      })



      .otherwise({
        redirectTo: '/listUsers'
      });

    }]);

})();

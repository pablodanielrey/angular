(function() {
    'use strict'
    var app = angular.module('issues')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/orders', {
         templateUrl: 'modules/orders/index.html',
         controller: 'OrdersCtrl',
         controllerAs: 'vm'
      })

      .when('/myOrders', {
         templateUrl: 'modules/myOrders/index.html',
         controller: 'MyOrdersCtrl',
         controllerAs: 'vm'
      })

      .when('/logout', {
         templateUrl: 'modules/logout.html',
         controller: 'LogoutCtrl'
      })

      .otherwise({
        redirectTo: '/orders'
      });

    }]);

})();

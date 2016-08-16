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


      .when('/myOrdersList', {
         templateUrl: 'modules/myOrders/list/index.html',
         controller: 'MyOrdersListCtrl',
         controllerAs: 'vm'
      })

      .when('/myOrdersCreate', {
         templateUrl: 'modules/myOrders/create/create.html',
         controller: 'MyOrdersCreateCtrl',
         controllerAs: 'vm'
      })

      .when('/myOrdersDetail/:issueId', {
         templateUrl: 'modules/myOrders/detail/index.html',
         controller: 'myOrdersDetailCtrl',
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


var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/orders', {
     templateUrl: '/systems/pedidos/modules/orders/index.html',
     controller: 'OrdersCtrl',
     controllerAs: 'vm'
  })

  .when('/myOrders', {
     templateUrl: '/systems/pedidos/modules/myOrders/index.html',
     controller: 'MyOrdersCtrl',
     controllerAs: 'vm'
  })


  .when('/logout', {
     templateUrl: '/systems/login/modules/logout.html',
     controller: 'LogoutCtrl'
  })

  .otherwise({
    redirectTo: '/orders'
  });

}]);

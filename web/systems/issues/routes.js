

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider
    .when('/request', {
      controller: 'NewRequestCtrl',
      templateUrl: '/systems/issues/modules/newRequest/index.html'
    })
    
    .otherwise({
        redirectTo: '/request'
    });


}]);

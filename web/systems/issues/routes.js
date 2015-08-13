

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider
  
    .when('/request', {
      controller: 'NewRequestCtrl',
      templateUrl: '/systems/issues/modules/newRequest/index.html'
    })
    
    .when('/manage', {
      controller: 'ManageIssuesCtrl',
      templateUrl: '/systems/issues/modules/manageIssues/index.html'
    })
    
    .otherwise({
        redirectTo: '/request'
    });


}]);

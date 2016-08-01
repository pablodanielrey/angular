angular
.module('mainApp')
.config(['$routeProvider', function($routeProvider) {

  $routeProvider
  .when('/myfirstmodule', { templateUrl: 'modules/myfirstmodule/myfirstmodule.html', controller:'MyFirstModuleCtrl' })
  .when('/underconstruction', { templateUrl: 'modules/underconstruction/underconstruction.html'})

  .otherwise({ redirectTo: '/myfirstmodule' });
}]);


var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/', {
     templateUrl: '/systems/ingresantes/index.html',
     controller: 'IngresantesCtrl'
  })

  .otherwise({
    redirectTo: '/'
  });

}]);

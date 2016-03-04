
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  // .when('/main', {
  //    templateUrl: '/systems/laboralInsertion/modules/main.html'
  // })

  .when('/resetPassword', {
     templateUrl: '/systems/support/modules/resetPassword/index.html',
     controller: 'ResetPasswordCtrl'
  })

  .otherwise({
    redirectTo: '/resetPassword'
  });

}]);

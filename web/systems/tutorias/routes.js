
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/createTutoring', {
     templateUrl: '/systems/tutorias/modules/createTutoring/index.html',
     controller: 'CreateTutoringCtrl'
  })

  .when('/myTurorings', {
     templateUrl: '/systems/tutorias/modules/myTutorings/index.html',
     controller: 'MyTutoringsCtrl'
  })


  .when('/logout', {
     templateUrl: '/systems/login/modules/logout.html',
     controller: 'LogoutCtrl'
  })

  .otherwise({
    redirectTo: '/createTutoring'
  });

}]);

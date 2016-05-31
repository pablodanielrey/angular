
var app = angular.module('mainApp')

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/profile', {
     templateUrl: '/systems/fce/modules/perfil/index.html',
     controller: 'ProfileCtrl'
  })

  .when('/password', {
     templateUrl: '/systems/fce/modules/password/index.html',
     controller: 'PasswordCtrl'
  })

  .when('/mails', {
     templateUrl: '/systems/fce/modules/mails/index.html',
     controller: 'MailsCtrl'
  })

  .when('/systems', {
     templateUrl: '/systems/fce/modules/systems/index.html',
     controller: 'SystemsCtrl'
  })

  .when('/logout', {
     templateUrl: '/systems/login/modules/logout.html',
     controller: 'LogoutCtrl'
  })

  .otherwise({
    redirectTo: '/profile'
  });

}]);

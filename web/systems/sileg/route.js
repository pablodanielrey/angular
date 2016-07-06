angular
.module('mainApp')
.config(['$routeProvider', function($routeProvider) {

  $routeProvider
  .when('/adminDesignation', { templateUrl: 'modules/admindesignation/admindesignation.html', controller:'AdminDesignationCtrl' })

  .otherwise({ redirectTo: '/adminDesignation' });
}]);

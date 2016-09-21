angular
.module('mainApp')
.config(['$routeProvider', function($routeProvider) {

  $routeProvider
  .when('/addExtension', { templateUrl: 'modules/addextension/addextension.html', controller:'AddExtensionCtrl' })
  .when('/addProrogation', { templateUrl: 'modules/addprorogation/addprorogation.html', controller:'AddProrogationCtrl' })
  .when('/gridDesignation', { templateUrl: 'modules/griddesignation/griddesignation.html', controller:'GridDesignationCtrl' })

  .otherwise({ redirectTo: '/gridDesignation' });
}]);

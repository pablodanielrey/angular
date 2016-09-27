(function() {
    'use strict'
    var app = angular.module('assistance')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      /*
      .when('/create', {
         templateUrl: 'modules/offices/index.html',
         controller: 'OfficesCtrl',
         controllerAs: 'vm'
      })
	*/

      .otherwise({
        redirectTo: '/list'
      });

    }]);

})();

(function() {
    'use strict'
    var app = angular.module('tutorias.coordinadores')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/verTutorias', {templateUrl: 'modules/verTutorias/index.html', controller: 'VerTutoriasCtrl'})


      .otherwise({
        redirectTo: '/verTutorias'
      });

    }]);

})();

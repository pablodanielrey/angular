(function() {
    'use strict'
    var app = angular.module('tutorias.coordinadores')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/verTutorias', {templateUrl: 'modules/verTutorias/index.html', controller: 'VerTutoriasCtrl'})
      .when('/detailTutoria', {templateUrl: 'modules/detalleTutoria/index.html', controller: 'DetalleTutoriaCtrl'})


      .otherwise({
        redirectTo: '/verTutorias'
      });

    }]);

})();

angular
    .module('mainApp')
    .config(config);

config.$inject = ['$routeProvider'];

function config($routeProvider) {

  $routeProvider

    .when('/load', {
      templateUrl: '/systems/digesto/modules/createRegulation/createRegulation.html',
      controller: 'CreateRegulationCtrl',
    })
    .when('/search', {
      templateUrl: '/systems/digesto/modules/searchRegulation/searchRegulation.html',
      controller: 'SearchRegulationCtrl',
    })

    .otherwise({
        redirectTo: '/load'
    });

}

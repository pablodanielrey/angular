angular
    .module('mainApp')
    .config(configApp);

config.$inject = ['$routeProvider'];

function configApp($routeProvider) {

  $routeProvider

    .when('/load/:id/operation/:operation', {
      templateUrl: '/systems/digesto/modules/createRegulation/createRegulation.html',
      controller: 'CreateRegulationCtrl',
    })
    .when('/load/', {
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

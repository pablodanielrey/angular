angular
    .module('mainApp')
    .config(config);

config.$inject = ['$routeProvider'];

function config($routeProvider) {

  $routeProvider

    .when('/digesto', {
      templateUrl: '/modules/systems/digesto/index.html',
      controller: '..Controller',
      controllerAs: 'vm'
    })

    .when('/digesto2', {
      templateUrl: '/modules/systems/digesto/index2.html',
      controller: '..Controller',
      controllerAs: 'vm'
    })

    .otherwise({
        redirectTo: '/digesto'
    });

}

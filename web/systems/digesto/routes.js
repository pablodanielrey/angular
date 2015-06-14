angular
    .module('mainApp')
    .config(config);

config.$inject = ['$routeProvider'];

function config($routeProvider) {

  $routeProvider

    .when('/load', {
      templateUrl: '/systems/digesto/modules/create/index.html',
      controller: 'CreateDigestoController'
    })

    .when('/search', {
      templateUrl: '/systems/digesto/modules/search/index.html',
      controller: 'SearchDigestoController',
    })

    .otherwise({
        redirectTo: '/'
    });

}

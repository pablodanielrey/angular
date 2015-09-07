angular
    .module('mainApp')
    .config(config);

config.$inject = ['$routeProvider'];

function config($routeProvider) {

  $routeProvider

    .when('/live', {
      templateUrl: '/systems/camaras/modules/live/live.html',
      controller: 'createRegulation'
    })
    .when('/rec', {
      templateUrl: '/systems/camaras/modules/rec/rec.html',
      controller: 'RecordController'
    })

    .otherwise({
        redirectTo: '/'
    });

}

angular
    .module('mainApp')
    .config(config);

config.$inject = ['$routeProvider'];

function config($routeProvider) {

  $routeProvider

    .when('/firmware', {
      templateUrl: '/modules/systems/firmware/index.html',
      controller: 'MainFirmwareController',
      controllerAs: 'vm'
    })


    .when('/enroll', {
      templateUrl: '/modules/systems/firmware/enroll.html',
      controller: 'EnrollCtrl'
    })


    .when('/log', {
      templateUrl: '/modules/systems/firmware/log.html',
      controller: 'LogController',
      controllerAs: 'vm'
    })

    .otherwise({
        redirectTo: '/firmware'
    });

}

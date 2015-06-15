angular
    .module('mainApp')
    .config(config);

config.$inject = ['$routeProvider'];

function config($routeProvider) {

  $routeProvider

    .when('/firmware', {
      templateUrl: '/systems/firmware/modules/index.html',
      controller: 'MainFirmwareController',
      controllerAs: 'vm'
    })


    .when('/enroll', {
      templateUrl: '/systems/firmware/modules/enroll.html',
      controller: 'EnrollCtrl'
    })


    .when('/log', {
      templateUrl: '/systems/firmware/modules/log.html',
      controller: 'LogController',
      controllerAs: 'vm'
    })

    .otherwise({
        redirectTo: '/firmware'
    });

}

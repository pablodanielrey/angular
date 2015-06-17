angular
  .module('mainApp')
  .config(config);

config.$inject = ['$routeProvider'];

function config($routeProvider) {

  $routeProvider

    .when('/offices', {
      templateUrl: '/systems/offices/modules/index.html',
      controller: 'MainOfficeController',
      controllerAs: 'vm'
    })

    .otherwise({
        redirectTo: '/offices'
    });
}

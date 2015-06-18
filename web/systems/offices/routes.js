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

    .when('/usersOffices', {
      templateUrl: '/systems/offices/modules/usersOffices.html',
      controller: 'UsersOfficesController',
      controllerAs: 'vm'
    })

    .when('/rolesOffices', {
      templateUrl: '/systems/offices/modules/rolesOffices.html',
      controller: 'RolesOfficesController',
      controllerAs: 'vm'
    })

    .otherwise({
        redirectTo: '/offices'
    });
}

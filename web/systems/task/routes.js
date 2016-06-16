angular
    .module('mainApp')
    .config(configApp);

config.$inject = ['$routeProvider'];

function configApp($routeProvider) {

  $routeProvider

    
    .when('/myTask', {
      controller: 'MyTaskCtrl',
      templateUrl: '/systems/task/modules/myTask/index.html'
    })

    .otherwise({
        redirectTo: '/myTask'
    });
}
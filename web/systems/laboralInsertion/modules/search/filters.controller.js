angular
  .module('mainApp')
  .controller('FiltersCtrl', FiltersCtrl);

FiltersCtrl.$inject = ['$rootScope','$scope'];

function FiltersCtrl($rootScope, $scope) {

  $scope.model = {
    filters: []
  }

  $scope.view = {
    degrees:[
      {name: 'Seleccionar ...', value:'empty'},
      {name:'Contador Público',value:'contador'},
      {name: 'Lic. en Economía', value:'economia'},
      {name: 'Lic. en Administración', value:'administracion'}
    ]
  }

  /*
    filter {
      name: '',
      values: []
    }
  */

  console.log("hola");

}

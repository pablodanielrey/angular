angular
  .module('mainApp')
  .controller('FiltersCtrl', FiltersCtrl);

FiltersCtrl.$inject = ['$rootScope','$scope'];

function FiltersCtrl($rootScope, $scope) {

  $scope.model = {
    filters: [],
    selectFilterDate: null
  }

  $scope.view = {
    degrees:[
      {type:"filterDegree", name: 'Seleccionar ...', value:'empty'},
      {type:"filterDegree", name:'Contador Público',value:'contador'},
      {type:"filterDegree", name: 'Lic. en Economía', value:'economia'},
      {type:"filterDegree", name: 'Lic. en Administración', value:'administracion'}
    ],
    filtersDate: [
      {type:"filterDate",descriptionType:'Fecha de Inscripción', name:"2015", value:"2015"},
      {type:"filterDate",descriptionType:'Fecha de Inscripción', name:"2014", value:"2014"},
      {type:"filterDate",descriptionType:'Fecha de Inscripción', name:"2013", value:"2013"},
      {type:"filterDate",descriptionType:'Fecha de Inscripción', name:"2012", value:"2012"},
      {type:"filterDate",descriptionType:'Fecha de Inscripción', name:"2011", value:"2011"}
    ]
  }



  /*
    filter {
      name: '',
      values: []
    }
  */

  $scope.addDateFilter = addDateFilter;
  $scope.removeFilter = removeFilter;

  function addDateFilter() {
    $scope.model.filters.push($scope.model.selectFilterDate);
    var i = $scope.view.filtersDate.indexOf($scope.model.selectFilterDate);
    $scope.view.filtersDate.splice(i,1);
  }

  function removeFilter(filter) {

    switch (filter.type) {
      case "filterDate": $scope.view.filtersDate.push(filter); break;
    }
    var i = $scope.model.filters.indexOf(filter);
    $scope.model.filters.splice(i,1);    
  }

}

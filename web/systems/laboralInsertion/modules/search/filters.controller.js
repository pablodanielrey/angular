angular
  .module('mainApp')
  .controller('FiltersCtrl', FiltersCtrl);

FiltersCtrl.$inject = ['$rootScope','$scope'];

function FiltersCtrl($rootScope, $scope) {

  $scope.model = {
    filters: [],
    selectFilterDate: null,
    selectFilterDegree: null,
    selectFilterLaboral: null,
    selectFilterGenre: null,
    selectFilterResidence: null,
    selectFilterOrigin: null,
    selectFilterTravel: null,
    selectFilterLanguage: null,
    selectFilterLanguageNivel: null,
    beginCountCathedra: 0,
    endCountCathedra: 10,
    beginAverageWithFails: 0,
    endAverageWithFails: 10,
    beginAverageWithoutFails: 0,
    endAverageWithoutFails: 10
  }

  $scope.view = {
    enabledFilterCountCathedra: true,
    enabledFilterAverageWithFails: true,
    enabledFilterAverageWithoutFails: true,
    filtersDegrees:[
      {type:"filterDegree", descriptionType:'Carrera', name:'Contador Público',value:'contador'},
      {type:"filterDegree", descriptionType:'Carrera', name: 'Lic. en Economía', value:'economia'},
      {type:"filterDegree", descriptionType:'Carrera', name: 'Lic. en Administración', value:'administracion'}
    ],
    filtersDate: [
      {type:"filterDate", descriptionType:'Fecha de Inscripción', name:"2015", value:"2015"},
      {type:"filterDate", descriptionType:'Fecha de Inscripción', name:"2014", value:"2014"},
      {type:"filterDate", descriptionType:'Fecha de Inscripción', name:"2013", value:"2013"},
      {type:"filterDate", descriptionType:'Fecha de Inscripción', name:"2012", value:"2012"},
      {type:"filterDate", descriptionType:'Fecha de Inscripción', name:"2011", value:"2011"}
    ],
    filtersLaboral: [
      {type:"filterLaboral", descriptionType:'Oferta Laboral', name:"Pasantía", value:"pasantia"},
      {type:"filterLaboral", descriptionType:'Oferta Laboral', name:"Full-Time", value:"fulltime"},
      {type:"filterLaboral", descriptionType:'Oferta Laboral', name:"Jovenes Profesionales", value:"jp"},
    ],
    filtersGenre: [
      {type:"filterGenre", descriptionType:'Sexo', name:"Masculino", value:"masculine"},
      {type:"filterGenre", descriptionType:'Sexo', name:"Femenino", value:"female"},
      {type:"filterGenre", descriptionType:'Sexo', name:"Otros", value:"other"}
    ],
    filtersResidence: [
      {type:"filterResidence", descriptionType:'Ciudad de Residencia', name:"La Plata", value:"laPlata"},
      {type:"filterResidence", descriptionType:'Ciudad de Residencia', name:"M.B Gonnet", value:"gonnet"},
      {type:"filterResidence", descriptionType:'Ciudad de Residencia', name:"Ranchos", value:"ranchos"},
      {type:"filterResidence", descriptionType:'Ciudad de Residencia', name:"City Bell", value:"cityBell"},
      {type:"filterResidence", descriptionType:'Ciudad de Residencia', name:"Otros", value:"others"}
    ],
    filtersOrigin: [
      {type:"filterOrigin", descriptionType:'Ciudad de Origen', name:"La Plata", value:"laPlata"},
      {type:"filterOrigin", descriptionType:'Ciudad de Origen', name:"M.B Gonnet", value:"gonnet"},
      {type:"filterOrigin", descriptionType:'Ciudad de Origen', name:"Ranchos", value:"ranchos"},
      {type:"filterOrigin", descriptionType:'Ciudad de Origen', name:"City Bell", value:"cityBell"},
      {type:"filterOrigin", descriptionType:'Ciudad de Origen', name:"Otros", value:"others"}
    ],
    filtersTravel: [
      {type:"filterTravel", descriptionType:'Viajar', name:"No", value:"no"},
      {type:"filterTravel", descriptionType:'Viajar', name:"Sí", value:"yes"}
    ],
    filtersLanguage: [
      {type:"filterLanguage", descriptionType:"Idioma", name:"Inglés", value:"english"},
      {type:"filterLanguage", descriptionType:"Idioma", name:"Postugués", value:"portuguese"}
    ],
    filtersLanguageNivel: [
      {type:"filterLanguageNivel", descriptionType:"Idioma", name:"Básico", value:"basic", order: 1},
      {type:"filterLanguageNivel", descriptionType:"Idioma", name:"Intermedio", value:"intermediate", order: 2},
      {type:"filterLanguageNivel", descriptionType:"Idioma", name:"Avanzado", value:"advanced", order: 3}
    ]
  }



  /*
    filter {
      name: '',
      values: []
    }
  */

  $scope.addDateFilter = addDateFilter;
  $scope.addDegreeFilter = addDegreeFilter;
  $scope.addLaboralFilter = addLaboralFilter;
  $scope.addGenreFilter = addGenreFilter;
  $scope.addResidenceFilter = addResidenceFilter;
  $scope.addOriginFilter = addOriginFilter;
  $scope.addTravelFilter = addTravelFilter;
  $scope.addLanguageFilter = addLanguageFilter;
  $scope.addCountCathedra = addCountCathedra;
  $scope.addAverageWithFails = addAverageWithFails;
  $scope.addAverageWithoutFails = addAverageWithoutFails;

  $scope.removeFilter = removeFilter;

  function addDateFilter() {
    if ($scope.model.selectFilterDate == null) {
      return;
    }
    $scope.model.filters.push($scope.model.selectFilterDate);
    var i = $scope.view.filtersDate.indexOf($scope.model.selectFilterDate);
    $scope.view.filtersDate.splice(i,1);
  }

  function addDegreeFilter() {
    if ($scope.model.selectFilterDegree == null) {
      return;
    }
    $scope.model.filters.push($scope.model.selectFilterDegree);
    var i = $scope.view.filtersDegrees.indexOf($scope.model.selectFilterDegree);
    $scope.view.filtersDegrees.splice(i,1);
  }

  function addLaboralFilter() {
    if ($scope.model.selectFilterLaboral == null) {
      return;
    }
    $scope.model.filters.push($scope.model.selectFilterLaboral);
    var i = $scope.view.filtersLaboral.indexOf($scope.model.selectFilterLaboral);
    $scope.view.filtersLaboral.splice(i,1);
  }

  function addGenreFilter() {
    if ($scope.model.selectFilterGenre == null) {
      return;
    }
    $scope.model.filters.push($scope.model.selectFilterGenre);
    var i = $scope.view.filtersGenre.indexOf($scope.model.selectFilterGenre);
    $scope.view.filtersGenre.splice(i,1);
  }

  function addResidenceFilter() {
    if ($scope.model.selectFilterResidence == null) {
      return;
    }
    $scope.model.filters.push($scope.model.selectFilterResidence);
    var i = $scope.view.filtersResidence.indexOf($scope.model.selectFilterResidence);
    $scope.view.filtersResidence.splice(i,1);
  }

  function addOriginFilter() {
    if ($scope.model.selectFilterOrigin == null) {
      return;
    }
    $scope.model.filters.push($scope.model.selectFilterOrigin);
    var i = $scope.view.filtersOrigin.indexOf($scope.model.selectFilterOrigin);
    $scope.view.filtersOrigin.splice(i,1);
  }

  function addTravelFilter() {
    if ($scope.model.selectFilterTravel == null) {
      return;
    }
    $scope.model.filters.push($scope.model.selectFilterTravel);
    var i = $scope.view.filtersTravel.indexOf($scope.model.selectFilterTravel);
    $scope.view.filtersTravel.splice(i,1);
  }

  function addLanguageFilter() {
    if ($scope.model.selectFilterLanguage == null) {
      return;
    }
    var l = $scope.model.selectFilterLanguage;
    l.nivel = $scope.model.selectFilterLanguageNivel.name;
    $scope.model.filters.push(l);
    var i = $scope.view.filtersLanguage.indexOf($scope.model.selectFilterLanguage);
    $scope.view.filtersLanguage.splice(i,1);
  }

  function addCountCathedra() {
    var b = $scope.model.beginCountCathedra;
    var e = $scope.model.endCountCathedra;
    var v = b + " - " + e;
    var filter = {type:"filterCountCathedra", descriptionType:'Cantidad de Materias', name: v , value: v};
    $scope.model.filters.push(filter);
    $scope.view.enabledFilterCountCathedra = false;
  }

  function addAverageWithFails() {
    var b = $scope.model.beginAverageWithFails;
    var e = $scope.model.endAverageWithFails;
    var v = b + " - " + e;
    var filter = {type:"filterAverageWithFails", descriptionType:'Promedio con aplazos', name: v , value: v};
    $scope.model.filters.push(filter);
    $scope.view.enabledFilterAverageWithFails = false;
  }

  function addAverageWithoutFails() {
    var b = $scope.model.beginAverageWithoutFails;
    var e = $scope.model.endAverageWithoutFails;
    var v = b + " - " + e;
    var filter = {type:"filterAverageWithoutFails", descriptionType:'Promedio sin aplazos', name: v , value: v};
    $scope.model.filters.push(filter);
    $scope.view.enabledFilterAverageWithoutFails = false;
  }


  function removeFilter(filter) {
    switch (filter.type) {
      case "filterDate": $scope.view.filtersDate.push(filter); break;
      case "filterDegree": $scope.view.filtersDegrees.push(filter); break;
      case "filterLaboral": $scope.view.filtersLaboral.push(filter); break;
      case "filterGenre": $scope.view.filtersGenre.push(filter); break;
      case "filterResidence": $scope.view.filtersResidence.push(filter); break;
      case "filterOrigin": $scope.view.filtersOrigin.push(filter); break;
      case "filterTravel": $scope.view.filtersTravel.push(filter); break;
      case "filterLanguage": $scope.view.filtersLanguage.push(filter); break;
      case "filterCountCathedra": $scope.view.enabledFilterCountCathedra = true;break;
      case "filterAverageWithFails": $scope.view.enabledFilterAverageWithFails = true;break;
      case "filterAverageWithoutFails": $scope.view.enabledFilterAverageWithoutFails = true;break;
    }
    var i = $scope.model.filters.indexOf(filter);
    $scope.model.filters.splice(i,1);
  }


}

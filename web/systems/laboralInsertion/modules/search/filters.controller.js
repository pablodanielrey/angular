angular
  .module('mainApp')
  .controller('FiltersCtrl', FiltersCtrl);

FiltersCtrl.$inject = ['$rootScope','$scope','$filter'];

function FiltersCtrl($rootScope, $scope, $filter) {

  $scope.model = {
    selectFilterDegree: null,
    selectFilterLaboral: null,
    selectWorkExperience: null,
    selectFilterGenre: null,
    selectFilterResidence: null,
    selectFilterOrigin: null,
    selectFilterTravel: null,
    selectFilterLanguage: null,
    selectFilterLanguageNivel: null,
    beginDate:null,
    endDate:new Date(),
    beginCountCathedra: 0,
    endCountCathedra: 10,
    beginAverageWithFails: 0,
    endAverageWithFails: 10,
    beginAverageWithoutFails: 0,
    endAverageWithoutFails: 10,
    filters: []
  }

  $scope.view = {
    enabledFilterCountCathedra: true,
    enabledFilterAverageWithFails: true,
    enabledFilterAverageWithoutFails: true,
    filtersDegrees:['Contador Público','Licenciatura en Economía','Licenciatura en Administración','Licenciatura en Turismo','Tecnicatura en Cooperativas'],
    filtersLaboral: ["Pasantía", "Full-Time", "Jovenes Profesionales"],
    filtersWorkExperience: ['No', 'Sí'],
    filtersGenre: ["Masculino", "Femenino", "Otros"],
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
  $scope.addWorkExperience = addWorkExperience;
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
    if ($scope.model.beginDate == null || $scope.model.endDate == null) {
      return;
    }
    // {'filter': 'FInscriptionDate', 'data': {'ffrom': '2016-03-18T12:38:40.720044', 'to': '2016-03-18T12:38:40.720099'}}
    var dateFilter = {};
    dateFilter.filter = 'FInscriptionDate';
    dateFilter.data = {};
    dateFilter.data.ffrom = $scope.model.beginDate;
    dateFilter.data.to = $scope.model.endDate;

    var filter = {};
    filter.data = dateFilter;
    var beginStr = $filter('date')(dateFilter.data.ffrom,'dd/MM/yyyy');
    var endStr = $filter('date')(dateFilter.data.to,'dd/MM/yyyy');
    filter.view = {type:'Inscripción',value: beginStr + ' hasta ' + endStr};
    $scope.model.filters.push(filter);
  }

  function addDegreeFilter() {
    if ($scope.model.selectFilterDegree == null) {
      return;
    }
    // {"data": {"degree": "Lic. En Economía"}, "filter": "FDegree"}
    var dataFilter = {};
    dataFilter.data = {degree:$scope.model.selectFilterDegree};
    dataFilter.filter = "FDegree";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type:'Carrera',value: $scope.model.selectFilterDegree};

    $scope.model.filters.push(filter);
    var i = $scope.view.filtersDegrees.indexOf($scope.model.selectFilterDegree);
    $scope.view.filtersDegrees.splice(i,1);
  }

  function addLaboralFilter() {
    if ($scope.model.selectFilterLaboral == null) {
      return;
    }
    // {"data": {"offer": "Pasantía"}, "filter": "FOffer"}
    var dataFilter = {};
    dataFilter.data = {offer: $scope.model.selectFilterLaboral};
    dataFilter.filter = "FOffer";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type: 'Oferta Laboral', value: $scope.model.selectFilterLaboral};

    $scope.model.filters.push(filter);
    var i = $scope.view.filtersLaboral.indexOf($scope.model.selectFilterLaboral);
    $scope.view.filtersLaboral.splice(i,1);
  }

  function addWorkExperience() {
    if ($scope.model.selectWorkExperience == null) {
      return;
    }
    var value = ($scope.model.selectWorkExperience == "No") ? false : true;
    // {"data": {"workExperience": "No"}, "filter": "FWorkExperience"}
    var dataFilter = {};
    dataFilter.data = {workExperience: value};
    dataFilter.filter = "FWorkExperience";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type: 'Experiencia Laboral', value: $scope.model.selectWorkExperience};

    $scope.model.filters.push(filter);
    var i = $scope.view.filtersWorkExperience.indexOf($scope.model.selectWorkExperience);
    $scope.view.filtersWorkExperience.splice(i,1);
  }

  function addGenreFilter() {
    if ($scope.model.selectFilterGenre == null) {
      return;
    }
    // {"data": {"genre": "Masculino"}, "filter": "FGenre"}
    var dataFilter = {};
    dataFilter.data = {genre: $scope.model.selectFilterGenre};
    dataFilter.filter = "FGenre";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type: 'Género', value: $scope.model.selectFilterGenre};

    $scope.model.filters.push(filter);
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
    l.value = l.value + "-" + $scope.model.selectFilterLanguageNivel.value;
    $scope.model.filters.push(l);
    var i = $scope.view.filtersLanguage.indexOf($scope.model.selectFilterLanguage);
    $scope.view.filtersLanguage.splice(i,1);
  }

  function addCountCathedra() {
    var b = $scope.model.beginCountCathedra;
    var e = $scope.model.endCountCathedra;
    var filter = {type:"filterCountCathedra", descriptionType:'Cantidad de Materias', name: b + " - " + e , value: b + "-" + e};
    $scope.model.filters.push(filter);
    $scope.view.enabledFilterCountCathedra = false;
  }

  function addAverageWithFails() {
    var b = $scope.model.beginAverageWithFails;
    var e = $scope.model.endAverageWithFails;
    var filter = {type:"filterAverageWithFails", descriptionType:'Promedio con aplazos', name: b + " - " + e , value: b + "-" + e};
    $scope.model.filters.push(filter);
    $scope.view.enabledFilterAverageWithFails = false;
  }

  function addAverageWithoutFails() {
    var b = $scope.model.beginAverageWithoutFails;
    var e = $scope.model.endAverageWithoutFails;
    var filter = {type:"filterAverageWithoutFails", descriptionType:'Promedio sin aplazos', name: b + " - " + e , value: b + "-" + e};
    $scope.model.filters.push(filter);
    $scope.view.enabledFilterAverageWithoutFails = false;
  }


  function removeFilter(filter) {
    switch (filter.data.filter) {
      case "FDegree": $scope.view.filtersDegrees.push(filter.view.value); break;
      case "FOffer": $scope.view.filtersLaboral.push(filter.view.value); break;
      case "FWorkExperience": $scope.view.filtersWorkExperience.push(filter.view.value); break;
      case "FGenre": $scope.view.filtersGenre.push(filter.view.value); break;
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

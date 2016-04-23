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
    endCountCathedra: 37,
    beginAge: 20,
    endAge: 30,
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
    filtersOrigin: ["La Plata","M.B Gonnet", "Ranchos", "City Bell", "Otros"],
    filtersResidence: ["Casco Urbano (LP)",
                    "City Bell (LP)",
                    "Villa Elisa (LP)",
                    "City Bell (LP)",
                    "Gonnet (LP)",
                    "Tolosa (LP)",
                    "Ringuelet (LP)",
                    "Barrio Jardin (LP)",
                    "Barrio Hipódromo (LP)",
                    "Los Hornos (LP)",
                    "Etcheverry (LP)",
                    "Lisandro Olmos (LP)",
                    "El Retiro (LP)",
                    "Abasto (LP)",
                    "Melchor Romero (LP)",
                    "Las Malvinas (LP)",
                    "La Cumbre (LP)",
                    "Las Quintas (LP)",
                    "Gambier (LP)",
                    "Parque Sicardi (LP)",
                    "Villa Montoro (LP)",
                    "Rufino de Elizalde (LP)",
                    "Villa Elvira (LP)",
                    "El Carmen (LP)",
                    "Arana (LP)",
                    "Villa Garibaldi (LP)",
                    "Casco Urbano (LP)",
                    "José Hernandez (LP)",
                    "Gorina (LP)",
                    "Arturo Segui (LP)",
                    "El Peligro",
                    "Capital Federal",
                    "Berisso",
                    "Ensenada",
                    "Chascomús",
                    "Quilmes",
                    "Magdalena",
                    "Berazategui",
                    "Avellaneda",
                    "Florencio Varela",
                    "Otro"],
    filtersTravel: ["No", "Sí"],
    filtersLanguage: ['Inglés','Portugués','Alemán','Ruso','Italiano','Francés','Chino','Japonés'],
    filtersLanguageNivel: ["Básico", "Intermedio", "Avanzado"]
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
  $scope.addAgeFilter = addAgeFilter;
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

  function addAgeFilter() {
    if ($scope.model.beginAge > $scope.model.endAge && $scope.model.endAge > 0) {
      return;
    }
    // {"data": {"beginAge": 20, endAge: 30}, "filter": "FAge"}
    var dataFilter = {};
    dataFilter.data = {beginAge: parseInt($scope.model.beginAge), endAge: parseInt($scope.model.endAge)};
    dataFilter.filter = "FAge";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type: "Edad", value: $scope.model.beginAge + " - " + $scope.model.endAge};

    $scope.model.filters.push(filter);
  }

  function addResidenceFilter() {
    if ($scope.model.selectFilterResidence == null) {
      return;
    }

    // {"data": {"city": "La Plata"}, "filter": "FResidence"}
    var dataFilter = {};
    dataFilter.data = {city: $scope.model.selectFilterResidence};
    dataFilter.filter = "FResidence";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type: "Ciudad de Residencia", value: $scope.model.selectFilterResidence};

    $scope.model.filters.push(filter);
    var i = $scope.view.filtersResidence.indexOf($scope.model.selectFilterResidence);
    $scope.view.filtersResidence.splice(i,1);
  }

  function addOriginFilter() {
    if ($scope.model.selectFilterOrigin == null) {
      return;
    }
    // {"data": {"city": "La Plata"}, "filter": "FOrigin"}
    var dataFilter = {};
    dataFilter.data = {city: $scope.model.selectFilterOrigin};
    dataFilter.filter = "FCity";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type: "Ciudad de Origen", value: $scope.model.selectFilterOrigin};

    $scope.model.filters.push(filter);
    var i = $scope.view.filtersOrigin.indexOf($scope.model.selectFilterOrigin);
    $scope.view.filtersOrigin.splice(i,1);
  }

  function addTravelFilter() {
    if ($scope.model.selectFilterTravel == null) {
      return;
    }
    var value = ($scope.model.selectFilterTravel == "No") ? false : true;
    // {"data": {"travel": "No"}, "filter": "FTravel"}
    var dataFilter = {};
    dataFilter.data = {travel: value};
    dataFilter.filter = "FTravel";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type: 'Viajar', value: $scope.model.selectFilterTravel};

    $scope.model.filters.push(filter);
    var i = $scope.view.filtersTravel.indexOf($scope.model.selectFilterTravel);
    $scope.view.filtersTravel.splice(i,1);

  }

  function addLanguageFilter() {
    if ($scope.model.selectFilterLanguage == null) {
      return;
    }

    // {"data": {"language": "Inglés", "nivel":"Básico"}, "filter": "FLanguage"}
    var dataFilter = {};
    dataFilter.data = {language: $scope.model.selectFilterLanguage, level: $scope.model.selectFilterLanguageNivel};
    dataFilter.filter = "FLanguage";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type: 'Idioma', value: $scope.model.selectFilterLanguage, level: $scope.model.selectFilterLanguageNivel};

    $scope.model.filters.push(filter);
  }

  function addCountCathedra() {
    if ($scope.model.beginCountCathedra > $scope.model.endCountCathedra) {
      return;
    }
    // {"data": {"begin": 0, end: 10}, "filter": "FCountCathedra"}
    var dataFilter = {};
    dataFilter.data = {begin: parseInt($scope.model.beginCountCathedra), end: parseInt($scope.model.endCountCathedra)};
    dataFilter.filter = "FCountCathedra";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type: "Cantidad de Materias", value: $scope.model.beginCountCathedra + " - " + $scope.model.endCountCathedra};

    $scope.model.filters.push(filter);
    $scope.view.enabledFilterCountCathedra = false;
  }

  function addAverageWithFails() {
    if ($scope.model.beginAverageWithFails > $scope.model.endAverageWithFails) {
      return;
    }
    // {"data": {"begin": 0, end: 10}, "filter": "FAverageFails"}
    var dataFilter = {};
    dataFilter.data = {begin: parseFloat($scope.model.beginAverageWithFails), end: parseFloat($scope.model.endAverageWithFails)};
    dataFilter.filter = "FAverageFails";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type: "Promedio con aplazos", value: $scope.model.beginAverageWithFails + " - " + $scope.model.endAverageWithFails};

    $scope.model.filters.push(filter);
    $scope.view.enabledFilterAverageWithFails = false;
  }

  function addAverageWithoutFails() {
    if ($scope.model.beginAverageWithoutFails > $scope.model.endAverageWithoutFails) {
      return;
    }
    // {"data": {"begin": 0, end: 10}, "filter": "FAverage"}
    var dataFilter = {};
    dataFilter.data = {begin: parseFloat($scope.model.beginAverageWithoutFails), end: parseFloat($scope.model.endAverageWithoutFails)};
    dataFilter.filter = "FAverage";

    var filter = {};
    filter.data = dataFilter;
    filter.view = {type: "Promedio sin aplazos", value: $scope.model.beginAverageWithoutFails + " - " + $scope.model.endAverageWithoutFails};

    $scope.model.filters.push(filter);
    $scope.view.enabledFilterAverageWithoutFails = false;
  }


  function removeFilter(filter) {
    switch (filter.data.filter) {
      case "FDegree": $scope.view.filtersDegrees.push(filter.view.value); break;
      case "FOffer": $scope.view.filtersLaboral.push(filter.view.value); break;
      case "FWorkExperience": $scope.view.filtersWorkExperience.push(filter.view.value); break;
      case "FGenre": $scope.view.filtersGenre.push(filter.view.value); break;
      case "FResidence": $scope.view.filtersResidence.push(filter.view.value); break;
      case "FCity": $scope.view.filtersOrigin.push(filter.view.value); break;
      case "FTravel": $scope.view.filtersTravel.push(filter.view.value); break;
      case "FCountCathedra": $scope.view.enabledFilterCountCathedra = true;break;
      case "FAverageFails": $scope.view.enabledFilterAverageWithFails = true;break;
      case "FAverage": $scope.view.enabledFilterAverageWithoutFails = true;break;
    }
    var i = $scope.model.filters.indexOf(filter);
    $scope.model.filters.splice(i,1);
  }


}

var app = angular.module('mainApp');

app.controller('AssistanceFailsFiltersCtrl', ["$scope", "$timeout", "Assistance", "Notifications", "Utils", function($scope, $timeout, Assistance, Notifications, Utils) {

  $scope.model = {
    searching: false,
    assistanceFails:[{}],
    failsType:[{}],
    periodicities:[],
    hoursOperators:[{}],
    filter:{
      failType:{},
      count:0,
      minutes:0,
      hours:0,
      periodicity:'',
      hoursOperator:null,
      begin: new Date(),
      end: new Date()
    }
  };

  $scope.initializeFailsType = function() {
    $scope.model.failsType = [];

    var t = {name:'No posee marcación',description:'No existe ninguna marcación para esa fecha',isHours:false};
    $scope.model.failsType.push(t);

    t = {name:'Sin horario de llegada',description:'Sin horario de llegada',isHours:false};
    $scope.model.failsType.push(t);

    t = {name:'Llegada tardía',description:'Llegada tardía',isHours:true};
    $scope.model.failsType.push(t);

    t = {name:'Sin horario de salida',description:'Sin horario de salida',isHours:false};
    $scope.model.failsType.push(t);

    t = {name:'Salida temprana',description:'Salida temprana',isHours:true};
    $scope.model.failsType.push(t);

    $scope.model.filter.failType = null;
  }

  $scope.initializeHoursOperator = function() {
    $scope.model.hoursOperators = [];
    $scope.model.hoursOperators.push({value:'>',name:'Mayor a'});
    $scope.model.hoursOperators.push({value:'=',name:'Igual a'});
    $scope.model.hoursOperators.push({value:'<',name:'Menor a'});
      $scope.model.filter.hoursOperator = $scope.model.hoursOperators[0];
  }

  $scope.initializeFilter = function() {
    $scope.model.filter.begin = new Date();
    $scope.model.filter.end = new Date();
    $scope.model.filter.count = 1;
    $scope.model.filter.minutes = 0;
    $scope.model.filter.hours = 0;
    $scope.initializeHoursOperator();
    $scope.initializeFailsType();
    $scope.model.periodicities = ['Semanal','Mensual','Anual'];
    $scope.model.periodicity = null;
  }

  $scope.initialize = function() {
    $scope.model.assistanceFails = [{}];
    $scope.initializeDate();
    $scope.initializeFilter();
  };

  $scope.correctDates = function() {
    $scope.model.filter.begin.setHours(0);
    $scope.model.filter.begin.setMinutes(0);
    $scope.model.filter.begin.setSeconds(0);
    $scope.model.filter.end.setHours(23);
    $scope.model.filter.end.setMinutes(59);
    $scope.model.filter.end.setSeconds(59);
  };

  $scope.initializeDate = function() {
    $scope.correctDates();
  };

  $scope.$watch('model.filter.begin', $scope.correctDates);
  $scope.$watch('model.filter.end', $scope.correctDates);


// ---------------------- INICIO de filtro --------------------

  $scope.addFailToUser = function(fail, failsCountByUser) {
    var fu = null;
    for (var i = 0; i < failsCountByUser.length; i++) {
      var f = failsCountByUser[i];
      if (fail.user.id == f.userId) {
        fu = f;
      }
    }
    if (fu == null) {
      fu = {userId:fail.user.id,fails:[]};
      failsCountByUser.push(fu);
    }
    fu.fails.push(fail);
  }

  // failsByUser {userId,count:0,fails:[]}
  $scope.filterWeekly = function(failsByUser) {
    // for (var i = 0; i < failsByUser)
    // console.log();


    if (f.count >= $scope.model.filter.count) {
          return f.fails;
    }
  }

  $scope.filterPeriodicity = function(failByUser) {
    var fails = [];

    if ($scope.model.filter.periodicity == null) {
      if ($scope.model.filter.count < r.fails.length) {
        return f.fails;
      }
    }

    if ($scope.model.filter.periodicity == 'Semanal') {
      // failsFilters = failsFilters.concat($scope.filterWeekly(f));
    }
    return [];
  }

  $scope.filter = function(fails) {
    var failsFilters = [];
    var failsCountByUser = [{}]; // {userId:id,count:0,fails:[]}

    var diffInput = parseInt($scope.model.filter.hours * 60) + parseInt($scope.model.filter.minutes);

    for (var i = 0; i < fails.length; i++) {
      var r = fails[i];
      if ($scope.model.filter.failType == null || $scope.model.filter.failType.description == r.fail.description) {
          //chequeo la cantidad de horas de diferencia
          var diffMin = r.fail.seconds / 60;
          if (diffInput < diffMin) {
            $scope.addFailToUser(r,failsCountByUser);
          }
      }
    }

    for (var i = 0; i < failsCountByUser.length; i++) {
      var f = failsCountByUser[i];
      failsFilters = failsFilters.concat($scope.filterPeriodicity(f));
    }

    return failsFilters;
  }

  // ------------------------- Fin del filtro -----------------------------

  $scope.search = function() {
    $scope.model.searching = true;
    $scope.model.assistanceFails = [{}];
    $scope.initializeDate();

    // seteo los parametros del filtro
    var filterSearch = {};
    // Tipo de falla
    if ($scope.model.filter.failType == null) {
      filterSearch.failType = null;
    } else {
      filterSearch.failType = $scope.model.filter.failType.description;
    }
    // Cantidad
    filterSearch.count = $scope.model.filter.count;
    // Minutos totales
    filterSearch.minutes = (parseInt($scope.model.filter.hours) * 60) + parseInt($scope.model.filter.minutes);
    // Operador de las horas (<,>, =)
    if ($scope.model.filter.failType != null && $scope.model.filter.failType.isHours) {
      filterSearch.hoursOperator = $scope.model.filter.hoursOperator.value;
    }
    // Periodicidad
    filterSearch.periodicity = $scope.model.filter.periodicity;
    // Fecha de inicio
    filterSearch.begin = $scope.model.filter.begin;
    // Fecha de finalización
    filterSearch.end = $scope.model.filter.end;

    console.log(filterSearch);

    Assistance.getFailsByDate($scope.model.filter.begin, $scope.model.filter.end,
      function(response) {
        // var fails = $scope.filter(response);
        var fails = response;
        for (var i = 0; i < fails.length; i++) {
          var r = fails[i];

          var date = new Date(r.fail.date);
          r.fail.dateFormat = Utils.formatDate(date);
          r.fail.dateExtend = Utils.formatDateExtend(date);

          if (r.fail.startSchedule || r.fail.endSchedule) {
            r.fail.dateSchedule = (r.fail.startSchedule) ? r.fail.startSchedule : r.fail.endSchedule;
            r.fail.dateSchedule = Utils.formatTime(new Date(r.fail.dateSchedule));
          }

          //esto es de prueba
          // r.fail.start = r.fail.date;

          if (r.fail.start || r.fail.end) {
            r.fail.wh = (r.fail.start) ?  new Date(r.fail.start) : new Date(r.fail.end);
            r.fail.wh =  Utils.formatTime(r.fail.wh);
          }

          // esto es de prueba
          // r.fail.seconds = 3825;

          if (r.fail.seconds) {
            var hoursDiff = Math.floor((r.fail.seconds / 60) / 60);
            var minutesDiff = Math.floor((r.fail.seconds / 60) % 60);
            r.fail.diff = ('0' + hoursDiff).substr(-2) + ":" + ('0' + minutesDiff).substr(-2);
          }

          $scope.model.assistanceFails.push(r);
        }
        $scope.predicate = 'user.dni';
        $scope.model.searching = false;
      },
      function(error) {
        $scope.model.searching = false;
        Notifications.message(error);
      }

    );
  };

  $timeout(function() {
    $scope.initialize();
  }, 0);

}]);

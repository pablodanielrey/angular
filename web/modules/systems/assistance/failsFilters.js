var app = angular.module('mainApp');

app.controller('AssistanceFailsFiltersCtrl', ["$scope", "$timeout", "Assistance", "Notifications", "Utils", function($scope, $timeout, Assistance, Notifications, Utils) {

  $scope.model = {
    searching: false,
    begin: new Date(),
    end: new Date(),
    assistanceFails:[{}],
    typeFails:[{}],
    filter:{failType:{}}
  };

  $scope.initializeTypeFails = function() {
    $scope.model.typeFails = [];

    var t = {name:'No posee marcación',description:'No existe ninguna marcación para esa fecha'};
    $scope.model.typeFails.push(t);

    t = {name:'Sin horario de llegada',description:'Sin horario de llegada'};
    $scope.model.typeFails.push(t);

    t = {name:'Llegada tardía',description:'Llegada tardía'};
    $scope.model.typeFails.push(t);

    t = {name:'Sin horario de salida',description:'Sin horario de salida'};
    $scope.model.typeFails.push(t);

    t = {name:'Salida temprana',description:'Salida temprana'};
    $scope.model.typeFails.push(t);

    $scope.model.filter.failType = null;
  }

  $scope.initializeFilter = function() {
    $scope.model.filter.count = 1;
    $scope.model.filter.minutes = 0;
    $scope.model.filter.hours = 0;
    $scope.initializeTypeFails();
  }

  $scope.initialize = function() {
    $scope.model.begin = new Date();
    $scope.model.end = new Date();
    $scope.model.assistanceFails = [{}];
    $scope.initializeDate();
    $scope.initializeFilter();
  };

  $scope.correctDates = function() {
    $scope.model.begin.setHours(0);
    $scope.model.begin.setMinutes(0);
    $scope.model.begin.setSeconds(0);
    $scope.model.end.setHours(23);
    $scope.model.end.setMinutes(59);
    $scope.model.end.setSeconds(59);
  };

  $scope.initializeDate = function() {
    $scope.correctDates();
  };

  $scope.$watch('model.begin', $scope.correctDates);
  $scope.$watch('model.end', $scope.correctDates);


  $scope.addFailToUser = function(fail, failsCountByUser) {
    var fu = null;
    for (var i = 0; i < failsCountByUser.length; i++) {
      var f = failsCountByUser[i];
      if (fail.user.id == f.userId) {
        fu = f;
      }
    }
    if (fu == null) {
      fu = {userId:fail.user.id,
            count:0,
            fails:[]};
      failsCountByUser.push(fu);
    }

    fu.count = fu.count + 1;
    fu.fails.push(fail);
  }

  $scope.filter = function(fails) {
    var failsFilters = [];
    var failsCountByUser = [{}]; // {userId:id,count:0,fails:[]}

    var diffInput = parseInt($scope.model.filter.hours * 60) + parseInt($scope.model.filter.minutes);
    console.log("DiffInput:" + diffInput);

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
      if (f.count >= $scope.model.filter.count) {
        failsFilters = failsFilters.concat(f.fails);
      }
    }

    return failsFilters;
  }

  $scope.search = function() {
    $scope.model.searching = true;
    $scope.model.assistanceFails = [{}];
    $scope.initializeDate();
    Assistance.getFailsByDate($scope.model.begin, $scope.model.end,
      function(response) {
        var fails = $scope.filter(response);
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

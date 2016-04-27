angular
  .module('mainApp')
  .controller('RequestCtrl', RequestCtrl);

RequestCtrl.inject = ['$scope', 'Login', 'Assistance', '$location']

function RequestCtrl($scope, Login, Assistance, $location) {

  $scope.initialize = initialize;
  $scope.initializeFilters = initializeFilters;
  $scope.formatJustification = formatJustification;
  $scope.search = search;

  $scope.model = {
    userId: null,
    start: null,
    end: null,
    justifications: []
  }

  $scope.view = {
    searching: false
  }

  const dayMillis = 24 * 60 * 60 * 1000;
  const limitDay = 6;

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.model.userId = '';
    Login.getSessionData()
      .then(function(s) {
          $scope.model.userId = s.user_id;
          $scope.initialize();
      }, function(err) {
        console.log("error");
      });
  });

  $scope.$watch(function() {return $scope.model.start;}, function(o,n) {
    if (n == null) {
      $scope.model.start = o;
    }
    if ($scope.model.start == null && $scope.model.end == null) {
        $scope.initializeFilters();
    }

    $scope.model.start = ($scope.model.start == null) ? new Date($scope.model.end.getTime() - (limitDay * dayMillis))  : $scope.model.start;
    $scope.model.end = ($scope.model.end <= $scope.model.start) ? $scope.model.start : $scope.model.end;

  });

  $scope.$watch(function() {return $scope.model.end;}, function(o,n) {
    if (n == null) {
      $scope.model.end = o;
    }
    if ($scope.model.start == null && $scope.model.end == null) {
        $scope.initializeFilters();
    }

    $scope.model.end = ($scope.model.end == null) ? new Date($scope.model.start.getTime() + (limitDay * dayMillis))  : $scope.model.end;
    $scope.model.start = ($scope.model.start >= $scope.model.end) ? new Date($scope.model.end.getTime() - (limitDay * dayMillis))  : $scope.model.start;
  });

  function initialize() {
    $scope.view.searching = false;
    $scope.model.justifications = [];
    $scope.initializeFilters();
  }

  function initializeFilters() {
    var now = new Date()
    // getDay obtiene el dia de la semana: 0->Domingo, 1->Lunes, ... , 6->Sábado
    var day = (now.getDay() - 1 < 0) ? limitDay : now.getDay() - 1;

    var start = new Date(now.getTime() - (day * dayMillis));

    end = new Date(start.getTime() + (limitDay * dayMillis));

    $scope.model.start = start;
    $scope.model.end = end;
  }

  function search() {
    if ($scope.model.start == null || $scope.model.end == null) {
      return
    }
    $scope.view.searching = true;
    Assistance.getJustifications($scope.model.userId, $scope.model.start, $scope.model.end, false).then(function(data) {
      $scope.view.searching = false;
      justifications = [];
      for (userId in data) {
        var just = data[userId];
        for (var i = 0; i < just.length; i++) {
          justifications.push($scope.formatJustification(just[i]));
        }
      }
      console.log(justifications);
      $scope.model.justifications = justifications;
    }, function(error) {
      $scope.view.searching = false;
      console.log('Error al buscar las justificaciones');
    });
  }


  function formatJustification(just) {
    var j = {};
    j.name = just.identifier;
    j.type = just.type;
    j.start = just.start;
    j.end = just.end;
    j.status = just.status.status;
    return j;
  }


}

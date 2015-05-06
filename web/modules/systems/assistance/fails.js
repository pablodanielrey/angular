var app = angular.module('mainApp');

app.controller('AssistanceFailsCtrl', ["$scope", "$timeout", "Assistance", "Notifications", "Utils","$filter", function($scope, $timeout, Assistance, Notifications, Utils, $filter) {

  $scope.model = {
    searching: false,
    begin: new Date(),
    end: new Date(),
    assistanceFails:[{}],
    justifications:[],
    base64:''
  };



  $scope.download = function() {
    if ($scope.model.base64 == null || $scope.model.base64 == '') {
      return;
    }
    var blob = Utils.base64ToBlob($scope.model.base64);
    window.saveAs(blob,'incumplimientos.ods');
  }


  // ordenacion

  $scope.orderBy = $filter('orderBy');

  $scope.order = function(predicate, reverse) {
    $scope.model.assistanceFails = $scope.orderBy($scope.model.assistanceFails, predicate, reverse);
  };

  //


  $scope.loadJustifications = function() {
    Assistance.getJustifications(
      function(justifications) {
        $scope.model.justifications = justifications;
      },
      function(err) {
        Notifications.message(err);
      }
    );
  }

  $scope.getJustificationById = function(id) {
    for (var i = 0; i < $scope.model.justifications.length; i++) {
      var j = $scope.model.justifications[i];
      if (j.id == id) {
        return j;
      }
    }
  }


  $scope.initialize = function() {
    $scope.model.begin = new Date();
    $scope.model.end = new Date();
    $scope.model.assistanceFails = [{}];
    $scope.initializeDate();
    $scope.loadJustifications();
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


  $scope.search = function() {
    $scope.model.searching = true;
    $scope.model.assistanceFails = [{}];
    $scope.initializeDate();
    Assistance.getFailsByDate($scope.model.begin, $scope.model.end,
      function(response) {
        $scope.model.base64 = response.base64;

        for (var i = 0; i < response.response.length; i++) {

          var r = response.response[i];

          r.justification = {name:''};
          if ((r.fail.justifications != undefined) && (r.fail.justifications != null) && (r.fail.justifications.length > 0)) {
            var just = r.fail.justifications[0];
            var j = $scope.getJustificationById(r.fail.justifications[0].justification_id);
            just.name = j.name;
            r.justification = just;
          }

          var date = new Date(r.fail.date);
          r.fail.dateFormat = Utils.formatDate(date);
          r.fail.dateExtend = Utils.formatDateExtend(date);
          r.fail.dayOfWeek = {};
          r.fail.dayOfWeek.name = Utils.getDayString(date);
          r.fail.dayOfWeek.number = date.getDay();



          if (r.fail.startSchedule || r.fail.endSchedule) {
            r.fail.dateSchedule = (r.fail.startSchedule) ? r.fail.startSchedule : r.fail.endSchedule;
            r.fail.dateSchedule = Utils.formatTime(new Date(r.fail.dateSchedule));
          }

          if (r.fail.start || r.fail.end) {
            r.fail.wh = (r.fail.start) ?  new Date(r.fail.start) : new Date(r.fail.end);
            r.fail.wh =  Utils.formatTime(r.fail.wh);
          }

          if (r.fail.seconds) {
            var hoursDiff = Math.floor((r.fail.seconds / 60) / 60);
            var minutesDiff = Math.floor((r.fail.seconds / 60) % 60);
            r.fail.diff = ('0' + hoursDiff).substr(-2) + ":" + ('0' + minutesDiff).substr(-2);
          }

          $scope.model.assistanceFails.push(r);
        }
        $scope.order(['fail.dateExtend','user.lastname','user.name'],false);//ordenamiento por defecto
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

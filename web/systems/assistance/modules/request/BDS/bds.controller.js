angular
  .module('mainApp')
  .controller('OTWithReturnCtrl', OTWithReturnCtrl);

OTWithReturnCtrl.inject = ['$rootScope', '$scope', 'Assistance', '$timeout']

function OTWithReturnCtrl($rootScope, $scope, Assistance, $timeout) {

  $scope.initialize = initialize;
  $scope.initializeDate = initializeDate;
  $scope.create = create;

  $scope.view = {
    styleStatus: '',
    statusOptions: ['solicitud', 'mensaje'],
    messageOptions: ['', 'procesando', 'procesado', 'sinDisponibilidad', 'errorDeSistema'],
    styleMessage: ''
  }

  $scope.model = {
    start: new Date(),
    end: new Date(),
    hours: 0,
    minutes: 0,
    limitMonth: '-',
    limitYear: '-'
  }

  $scope.$watch(function() {return $scope.model.hours;}, function(o,n) {
    if ($scope.model.hours >= 3) {
      $scope.model.minutes = 0;
      $scope.model.hours = 3;
    }

  });

  $scope.$watch(function() {return $scope.model.minutes;}, function(o,n) {
    if ($scope.model.minutes == 60) {
      $scope.model.minutes = 0;
      $scope.model.hours = $scope.model.hours + 1;
    }
    if ($scope.model.hours >= 3) {
      $scope.model.hours = 3;
      $scope.model.minutes = 0;
      return;
    }
  });

  function initialize(userId) {
    $scope.view.styleStatus = $scope.view.statusOptions[0];
    $scope.view.styleMessage = $scope.view.messageOptions[0];
    $scope.clazz = 'OutTicketWithReturnJustification';
    $scope.module = 'model.assistance.justifications.outTicketJustification';
    $scope.userId = userId;
    $scope.initializeDate();
  }

  function initializeDate() {
    $scope.model.start = new Date();
    $scope.model.end = new Date();
    $scope.model.hours = 0;
    $scope.model.minutes = 0;
  }

  $scope.$on('selectOTWithReturnEvent', function(e, userId) {
    $scope.initialize(userId);
  })

  function create() {
    $scope.view.styleStatus = $scope.view.statusOptions[1];
    $scope.view.styleMessage = $scope.view.messageOptions[1];
    end = new Date($scope.model.start);
    minutes = $scope.model.hours * 60 + $scope.model.minutes;
    end.setMinutes(end.getMinutes() + minutes);

    Assistance.createRangedTimeWithReturnJustification($scope.model.start, $scope.model.end, $scope.userId, $scope.clazz, $scope.module).then(function(data) {
      $scope.$apply(function() {
        $scope.view.styleMessage = $scope.view.messageOptions[2];
        $scope.$emit('finishCreationJEvent');
      });
    }, function(error) {
      $scope.$apply(function(){
        $scope.view.styleMessage = $scope.view.messageOptions[4];
      });
      $timeout(function() {
        $scope.view.styleStatus = $scope.view.statusOptions[0];
        $scope.view.styleMessage = $scope.view.messageOptions[0];
      }, 2500);
    });
  }

}

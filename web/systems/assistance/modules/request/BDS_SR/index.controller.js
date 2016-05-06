angular
  .module('mainApp')
  .controller('OTWithoutReturnCtrl', OTWithoutReturnCtrl);

OTWithoutReturnCtrl.inject = ['$rootScope', '$scope', 'Assistance', '$timeout']

function OTWithoutReturnCtrl($rootScope, $scope, Assistance, $timeout) {

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
    limitMonth: '-',
    limitYear: '-'
  }

  function initialize(userId) {
    $scope.view.styleStatus = $scope.view.statusOptions[0];
    $scope.view.styleMessage = $scope.view.messageOptions[0];
    $scope.clazz = 'OutTicketWithoutReturnJustification';
    $scope.module = 'model.assistance.justifications.outTicketJustification';
    $scope.userId = userId;
    $scope.initializeDate();
  }

  function initializeDate() {
    $scope.model.start = new Date();
    $scope.model.start.setHours(7);
    $scope.model.start.setMinutes(0);
    $scope.model.start.setSeconds(0);
    $scope.model.start.setMilliseconds(0);
  }

  $scope.$on('selectOTWithoutReturnEvent', function(e, userId) {
    $scope.initialize(userId);
  })

  function create() {
    $scope.view.styleStatus = $scope.view.statusOptions[1];
    $scope.view.styleMessage = $scope.view.messageOptions[1];

    console.log($scope.model.start);
    Assistance.createRangedTimeWithoutReturnJustification($scope.model.start, $scope.userId, $scope.clazz, $scope.module).then(function(data) {
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

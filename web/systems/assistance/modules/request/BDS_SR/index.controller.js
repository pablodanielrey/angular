angular
  .module('mainApp')
  .controller('OTWithoutReturnCtrl', OTWithoutReturnCtrl);

OTWithoutReturnCtrl.inject = ['$rootScope', '$scope', 'Assistance', '$timeout']

function OTWithoutReturnCtrl($rootScope, $scope, Assistance, $timeout) {

  $scope.initialize = initialize;
  $scope.initializeDate = initializeDate;
  $scope.create = create;
  $scope.loadJustificationData = loadJustificationData;

  $scope.view = {
    styleStatus: '',
    statusOptions: ['solicitud', 'mensaje'],
    messageOptions: ['', 'procesando', 'procesado', 'sinDisponibilidad', 'errorDeSistema'],
    styleMessage: ''
  }

  $scope.model = {
    start: new Date(),
    millisAvailables: 180,
    justificationData: {}
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
    $scope.model.justificationData = {mStock: '-', yStock: ''}
    $scope.loadJustificationData();
  }

  $scope.$on('selectOTWithoutReturnEvent', function(e, userId) {
    $scope.initialize(userId);
  })

  function loadJustificationData() {
    if ($scope.model.start == null) {
      return;
    }

    Assistance.getJustificationData($scope.userId, $scope.model.start, $scope.clazz, $scope.module).then(function(data) {
      if (data != null) {
        $scope.model.justificationData = data;

        minutes = Math.floor(data.mStock / 60);
        mhs = '0' + (Math.floor(minutes / 60)).toString();
        mmin = '0' + (minutes % 60).toString();
        $scope.model.justificationData.mStock = {hs: mhs.substr(-2, 2), min: mmin.substr(-2, 2)};

        $scope.model.millisAvailables = minutes * 60 * 1000 ;

        yMinutes = Math.floor(data.yStock / 60);
        yhs = '0' + (Math.floor(yMinutes / 60)).toString();
        ymin = '0' + (yMinutes % 60).toString();
        $scope.model.justificationData.yStock = {hs: yhs.substr(-2, 2), min: ymin.substr(-2, 2)};
      } else {
        $scope.model.justificationData = {mStock: '-', yStock: ''};
      }
    }, function(error) {
      $scope.model.justificationData = {mStock: '-', yStock: ''};
    });
  }

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

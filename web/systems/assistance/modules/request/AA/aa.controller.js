angular
  .module('mainApp')
  .controller('InformedAbsenceCtrl', InformedAbsenceCtrl);

InformedAbsenceCtrl.inject = ['$rootScope', '$scope', 'Assistance', '$timeout']

function InformedAbsenceCtrl($rootScope, $scope, Assistance, $timeout) {
  $scope.initialize = initialize;
  $scope.create = create;
  $scope.loadJustificationData = loadJustificationData;

  $scope.view = {
    styleStatus: '',
    statusOptions: ['solicitud', 'mensaje'],
    messageOptions: ['', 'procesando', 'procesado', 'sinDisponibilidad', 'errorDeSistema'],
    styleMessage: ''
  }

  $scope.model = {
    date: new Date(),
    justificationData: {}
  }

  function initialize(userId) {
    $scope.view.styleStatus = $scope.view.statusOptions[0];
    $scope.view.styleMessage = $scope.view.messageOptions[0];
    $scope.model.date = new Date();
    $scope.clazz = 'InformedAbsenceJustification';
    $scope.module = 'model.assistance.justifications.informedAbsenceJustification';
    $scope.userId = userId;
    $scope.loadJustificationData();
    $scope.model.justificationData = {mStock: '-', yStock: ''}
  }

  $scope.$on('selectInformedAbsenceEvent', function(e, userId) {
    $scope.initialize(userId);
  })

  $scope.$watch(function() {return $scope.model.date;}, function(o,n) {
    if (n == null) {
      $scope.model.date = o;
    }

    if (o == null || o.getMonth() != n.getMonth()) {
      $scope.loadJustificationData();
    }

  });

  function loadJustificationData() {
    if ($scope.model.date == null) {
      return;
    }

    Assistance.getJustificationData($scope.userId, $scope.model.date, $scope.clazz, $scope.module).then(function(data) {
      if (data != null) {
        $scope.model.justificationData = data;
      } else {
        $scope.model.justificationData = {mStock: '-', yStock: ''};
      }
    }, function(error) {
      $scope.model.justificationData = {mStock: '-', yStock: ''};
    });
  }

  function create() {
    console.log('create');
    $scope.view.styleStatus = $scope.view.statusOptions[1];
    $scope.view.styleMessage = $scope.view.messageOptions[1];
    Assistance.createSingleDateJustification($scope.model.date, $scope.userId, $scope.clazz, $scope.module).then(function(data) {
      $scope.$apply(function(){
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

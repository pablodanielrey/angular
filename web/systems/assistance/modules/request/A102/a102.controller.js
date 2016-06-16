angular
  .module('mainApp')
  .controller('A102Ctrl', A102Ctrl);

A102Ctrl.inject = ['$rootScope', '$scope', 'Assistance', '$timeout']

function A102Ctrl($rootScope, $scope, Assistance, $timeout) {

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
    justificationData: {stock:0}
  }

  function initialize(userId) {
    $scope.view.styleStatus = $scope.view.statusOptions[0];
    $scope.view.styleMessage = $scope.view.messageOptions[0];
    $scope.model.date = new Date();
    $scope.clazz = 'Art102Justification';
    $scope.module = 'model.assistance.justifications.art102Justification';
    $scope.userId = userId;
    $scope.loadJustificationData();
  }

  $scope.$on('selectA102Event', function(e, userId) {
    $scope.initialize(userId);
  })

  function loadJustificationData() {
    if ($scope.model.date == null) {
      return;
    }

    Assistance.getJustificationData($scope.userId, $scope.model.date, $scope.clazz, $scope.module).then(function(data) {
      if (data != null) {
        if (data.stock == undefined) {
          data.stock = 0;
        }
        $scope.model.justificationData = data;
      } else {
        $scope.model.justificationData = {stock: 0};
      }
    }, function(error) {
      $scope.model.justificationData = {stock: 0};
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

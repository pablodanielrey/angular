angular
  .module('mainApp')
  .controller('InformedAbsenceCtrl', InformedAbsenceCtrl);

InformedAbsenceCtrl.inject = ['$rootScope', '$scope', 'Assistance', '$timeout']

function InformedAbsenceCtrl($rootScope, $scope, Assistance, $timeout) {
  $scope.initialize = initialize;
  $scope.create = create;

  $scope.view = {
    styleStatus: '',
    statusOptions: ['solicitud', 'mensaje'],
    messageOptions: ['', 'procesando', 'procesado', 'sinDisponibilidad', 'errorDeSistema'],
    styleMessage: ''
  }

  $scope.model = {
    date: new Date()
  }

  function initialize(userId) {
    $scope.view.styleStatus = $scope.view.statusOptions[0];
    $scope.view.styleMessage = $scope.view.messageOptions[0];
    $scope.model.date = new Date();
    $scope.clazz = 'InformedAbsenceJustification';
    $scope.module = 'model.assistance.justifications.informedAbsenceJustification';
    $scope.userId = userId;
  }

  $scope.$on('selectInformedAbsenceEvent', function(e, userId) {
    $scope.initialize(userId);
  })

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

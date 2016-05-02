angular
  .module('mainApp')
  .controller('CompensatoryCtrl', CompensatoryCtrl);

CompensatoryCtrl.inject = ['$rootScope', '$scope', 'Assistance']

function CompensatoryCtrl($rootScope, $scope, Assistance) {

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
    $scope.clazz = 'CompensatoryJustification';
    $scope.module = 'model.assistance.justifications.compensatoryJustification';
    $scope.userId = userId;
  }

  $scope.$on('selectCompensatoryEvent', function(e, userId) {
    $scope.initialize(userId);
  })

  function create() {
    console.log('create');
    $scope.view.styleStatus = $scope.view.statusOptions[1];
    $scope.view.styleMessage = $scope.view.messageOptions[1];
    Assistance.createSingleDateJustification($scope.model.date, $scope.userId, $scope.clazz, $scope.module).then(function(data) {
      $scope.$apply(function(){$scope.view.styleMessage = $scope.view.messageOptions[2]});
    }, function(error) {
      $scope.view.styleMessage = $scope.view.messageOptions[4];
    });
  }

}

angular
  .module('mainApp')
  .controller('InscriptionCtrl', InscriptionCtrl);

InscriptionCtrl.inject = ['$rootScope', '$scope', '$wamp','Session']

function InscriptionCtrl($rootScope, $scope, $wamp, Session) {

  $scope.model = {
    ci: 0,
    cr: 0,
    inscriptions: ['','registro'],
    registrations: ['','pantalla1','pantalla2','pantalla3']
  };

  $scope.changeInscription = function() {
    $scope.model.ci = ($scope.model.ci + 1) % $scope.model.inscriptions.length;
  }

  $scope.changeRegistration = function() {
    $scope.model.cr = ($scope.model.cr + 1) % $scope.model.registrations.length;
  }

  $scope.getInscriptionClazz = function() {
    return $scope.model.inscriptions[$scope.model.ci];
  }


  $scope.status = {

  };


  $scope.initialize = function(){


  };

  $scope.submit = function(){
  };

  $scope.process = function(){
  };


  $scope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });



};

angular
  .module('mainApp')
  .service('Inscription',Inscription);

Inscription.inject = ['$rootScope','$wamp','Session']

function Inscription($rootScope, $wamp, Session) {

  $scope.model = {
    ci: 0,
    cr: 0,
    inscriptions: ['','registro'],
    registrations: ['','pantalla1','pantalla2','pantalla3']
  };

  $scope.changeInscription = function() {
    $scope.model.ci = ($scope.model.ci + 1) % $scope.model.inscriptions.lenght();
  }

  $scope.changeRegistration = function() {
    $scope.model.cr = ($scope.model.cr + 1) % $scope.model.registrations.lenght();
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

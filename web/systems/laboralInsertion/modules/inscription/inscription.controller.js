angular
  .module('mainApp')
  .controller('InscriptionCtrl', InscriptionCtrl);

InscriptionCtrl.inject = ['$rootScope', '$scope', '$wamp', 'LaboralInsertion', 'Login']

function InscriptionCtrl($rootScope, $scope, $wamp, LaboralInsertion, Login) {

  $scope.degrees = ['Contador Público', 'Licenciatura en Administración', 'Licenciatura en Turismo', 'Licenciatura en Economía', 'Tecnicatura en Cooperativas'];
  $scope.workTypes = ['Pasantía','Full-Time','Programa estudiantes avanzados y jovenes profesionales'];
  $scope.travel = ['No', 'Sí'];
  $scope.languages = ['Inglés','Portugués','Otro'];

  $scope.model = {
    ci: 0,
    cr: 0,
    inscriptions: ['','registro'],
    registrations: ['pantalla1','pantalla2','pantalla3','pantalla4','pantalla5','pantalla6','pantalla7'],
    currentPage: 1,
    inscriptionsData: [],

    // inscripcion a ser subida al server.
    offer: {
      degree: $scope.degrees[0],
      average1: 0.0,
      average2: 0.0,
      approved: 0,
      workType: $scope.workTypes[0],
      travel: $scope.travel[0]
    },

    // lenguajes a ser subidos al servidor
    languages: []
  };


  // --- elementos graficos -----

  $scope.model.totalPages = $scope.model.registrations.length;

  $scope.changeInscription = function() {
    $scope.model.ci = ($scope.model.ci + 1) % $scope.model.inscriptions.length;
  }

  $scope.changeRegistration = function() {
    $scope.model.cr = ($scope.model.cr + 1) % $scope.model.registrations.length;
  }

  $scope.changePreviousRegistration = function() {
    $scope.model.cr = $scope.model.cr - 1;
  }

  $scope.getInscriptionClazz = function() {
    return $scope.model.inscriptions[$scope.model.ci];
  }

  $scope.getRegistrationClazz = function() {
    return $scope.model.registrations[$scope.model.cr];
  }


  // --- modelo ---

  $scope.getInscriptions = function() {
    var userId = Login.getUserId();
    LaboralInsertion.findAllByUser(userId, function(data) {
      //$scope.model.inscriptionsData = data.inscriptions;
      $scope.model.inscriptionsData = [{
        'id':'sdfdsfdsfs',
        'languages':[{
            'id':'dsfsdfsd',
            'name':'Inglés',
            'level':'Básico'
          },
          {
            'id':'dsfsdfsd',
            'name':'Inglés',
            'level':'Básico'
          }],
        'inscriptions':[
          {
            'degree':'',
            'average1':10,
            'average2':20,
            'courses':10,
            'workType':'Pasantía',
            'reside':'Sí',
            'travel':'No'
          }]
      }];
    }, function(err) {
      console.log(err);
    })
  }

  $scope.getType = function(i) {
    console.log(i);
    return i.inscriptions[0].workType;
  }

  $scope.downloadInscription = function(i) {
    console.log(i);
  }

  $scope.removeInscription = function(i) {
    console.log(i);
  }


  $scope.addLanguage = function() {
    $scope.model.languages.push({
        name: $scope.languages[0],
        level: 'Básico'
      });
  }

  $scope.status = {

  };


  $scope.initialize = function(){
    $scope.getInscriptions();
  };

  $scope.submit = function(){
  };

  $scope.process = function(){
  };


  $scope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });



};

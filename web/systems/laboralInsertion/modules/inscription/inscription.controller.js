angular
  .module('mainApp')
  .controller('InscriptionCtrl', InscriptionCtrl);

InscriptionCtrl.inject = ['$rootScope', '$scope', '$wamp', 'LaboralInsertion', 'Login']

function InscriptionCtrl($rootScope, $scope, $wamp, LaboralInsertion, Login) {

  $scope.degrees = ['Contador Público', 'Licenciatura en Administración', 'Licenciatura en Turismo', 'Licenciatura en Economía', 'Tecnicatura en Cooperativas'];
  $scope.workTypes = ['Pasantía','Full-Time','Programa estudiantes avanzados y jovenes profesionales'];
  $scope.travel = ['No', 'Sí'];
  $scope.languages = ['Inglés','Portugués','Alemán','Ruso','Italiano','Francés','Chino','Japonés'];

  $scope.model = {
    ci: 0,
    cr: 0,
    inscriptions: ['','registro'],
    registrations: ['pantalla1','pantalla2','pantalla3','pantalla4','pantalla5','pantalla6','pantalla7'],
    inscriptionsData: [],

    // datos de usuario
    user: {
      name:'',
      lastname:'',
      dni:'',
      telephone:'',
      movil:'',
      email:'',
      country:'',
      residence_city:'',
      birth_city:'',
      address:'',
      genre:'Género',
      birthdate: null,
      student_number:''
    },


    showInscription: false,

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

  // seteo los watchs.
  /*
  $scope.$watch(function() { return $scope.model.user.name; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.user.lastname; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.user.dni; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.user.telephone; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.user.movil; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.user.email; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.user.country; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.user.residence_city; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.user.birth_city; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.user.address; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.user.genre; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.birthdate; }, function(o,n) { $scope.checkUserData(o); });
  $scope.$watch(function() { return $scope.model.student_number; }, function(o,n) { $scope.checkUserData(o); });
*/




  // --- elementos graficos -----

  $scope.model.totalPages = $scope.model.registrations.length;

  $scope.startInscription = function() {
    $scope.model.ci = 1;
    $scope.model.cr = 0;
  }

  $scope.endInscription = function() {
    $scope.model.ci = 0;
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

  $scope.updateUserData = function() {
    $scope.model.showInscription = $scope.checkUserData();
    console.log('actualizarrr');
  }

  $scope.checkUserData = function() {
    var ok = true;

    ok = ok && $scope.dataBasic.name.$valid;
    ok = ok && $scope.dataBasic.lastname.$valid;
    ok = ok && $scope.dataBasic.dni.$valid;
    ok = ok && $scope.dataBasic.student_number.$valid;
    ok = ok && $scope.dataBasic.birthdate.$valid;
    ok = ok && $scope.dataBasic.genre.$valid;

    return ok;

    /*
    var u = $scope.model.user;

    if (u.name == undefined || u.name.match(/^[a-zA-Z ]*$/)) {
      $scope.model.userChecks.name = null;
    } else {
      $scope.model.userChecks.name = 'Error';
    }

    if (u.lastname == undefined || u.lastname.match(/^[a-zA-Z ]*$/)) {
      $scope.model.userChecks.lastname = null;
    } else {
      $scope.model.userChecks.lastname = 'Error';
    }
    */

    // aca faltan mas chequeos.

  }

  $scope.uploadInscription = function() {
    $scope.endInscription();
    $scope.model.inscriptionsData.push({
      'id': 'asdasds',
      'languages': $scope.model.languages,
      'inscriptions': [$scope.model.offer]
    });
  }

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
            'degree':'Licenciatura en Administracion',
            'average1':10,
            'average2':20,
            'courses':10,
            'workType':'Pasantía',
            'reside':'Sí',
            'travel':'No'
          }]
      },
      {
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
            'degree':'Contador Público',
            'average1':10,
            'average2':20,
            'courses':10,
            'workType':'Pasantía',
            'reside':'Sí',
            'travel':'No'
          }]
      },
      {
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
            'degree':'Contador Público',
            'average1':10,
            'average2':20,
            'courses':10,
            'workType':'Pasantía',
            'reside':'Sí',
            'travel':'No'
          }]
      },
      {
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
            'degree':'Contador Público',
            'average1':10,
            'average2':20,
            'courses':10,
            'workType':'Pasantía',
            'reside':'Sí',
            'travel':'No'
          }]
      },
      {
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
            'degree':'Contador Público',
            'average1':10,
            'average2':20,
            'courses':10,
            'workType':'Pasantía',
            'reside':'Sí',
            'travel':'No'
          }]
      }
      ];
    }, function(err) {
      console.log(err);
    })
  }

  $scope.getDegree = function(i) {
    return i.inscriptions[0].degree;
  }

  $scope.getType = function(i) {
    return i.inscriptions[0].workType;
  }

  $scope.downloadInscription = function(i) {
    console.log(i);
  }

  $scope.removeInscription = function(i) {
    console.log(i);
    var index = $scope.model.inscriptionsData.indexOf(i);
    $scope.model.inscriptionsData.splice(index,1);
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

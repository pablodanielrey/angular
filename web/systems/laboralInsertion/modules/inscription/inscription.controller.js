angular
  .module('mainApp')
  .controller('InscriptionCtrl', InscriptionCtrl);

InscriptionCtrl.inject = ['$rootScope', '$scope', '$wamp', 'LaboralInsertion', 'Login', 'Users', 'Student', 'Notifications']

function InscriptionCtrl($rootScope, $scope, $wamp, LaboralInsertion, Login, Users, Student, Notifications) {

  $scope.degrees = ['Contador Público', 'Licenciatura en Administración', 'Licenciatura en Turismo', 'Licenciatura en Economía', 'Tecnicatura en Cooperativas'];
  $scope.workTypes = ['Pasantía','Full-Time','Programa estudiantes avanzados y jovenes profesionales'];
  $scope.travel = ['No', 'Sí'];
  $scope.languages = ['Inglés','Portugués','Alemán','Ruso','Italiano','Francés','Chino','Japonés'];

  $scope.model = {
    ci: 0,
    cr: 0,
    showNext: false,
    inscriptions: ['','registro'],
    registrations: ['pantalla1','pantalla2','pantalla3','pantalla4','pantalla5','pantalla6','pantalla7'],
    inscriptionsData: [],

    // datos de usuario

    student: {
      studentNumber: ''
    },

    mails: {
      emails: []
    },

    telephones: {
      telephone:'',
      movil:''
    },

    user: {
      name:'',
      lastname:'',
      dni:'',
      country:'',
      residence_city:'',
      city:'',
      address:'',
      genre:'',
      birthdate: null
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

    laboralData: {
      accepted_conditions: false,
      cv: '',
      email: '',
      languages: []
    }


  };


  $scope.$watch(function() { return $scope.model.offer.degree; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.offer.average1; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.offer.average2; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.offer.aproved; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.laboralData.languages; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.laboralData.email; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.laboralData.cv; }, function(o,n) { $scope.checkInscriptionPreconditions(); });

  $scope.checkInscriptionPreconditions = function() {

    console.log('chequeando');
      var ok = true;
      var offer = $scope.model.offer;

      if ($scope.model.cr >= 0) {
        ok = ok && offer.degree != '';
      }

      if ($scope.model.cr >= 1) {
        ok = ok && offer.average1 >= 0;
        ok = ok && offer.average1 >= 0;

        if (offer.degree == 'Contador Público') {
          ok = ok && offer.aproved >= 20;
        }

        if (offer.degree == 'Licenciatura en Administración') {
          ok = ok && offer.aproved >= 25;
        }

        if (offer.degree == 'Licenciatura en Turismo') {
          ok = ok && offer.aproved >= 17;
        }

        if (offer.degree == 'Licenciatura en Economía') {
          ok = ok && offer.aproved >= 22;
        }

        if (offer.degree == 'Tecnicatura en Cooperativas') {
          ok = ok && offer.aproved >= 10;
        }
      }

      if ($scope.model.cr >= 4) {
        var languages = $scope.model.laboralData.languages
        for (var l = 0; l < languages.length; l++) {
          for (var i = l + 1; i < languages.length; i++) {
            if (languages[l].name == languages[i].name) {
              $scope.model.showNext = false;
              return;
            }
          }
        }
      }

      $scope.model.showNext = ok;
    }

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

    var ok = $scope.checkUserData();
    if (!ok) {
      Notifications.message('Por favor complete todos los campos requeridos');
      return;
    }

    $scope.model.ci = 1;
    $scope.model.cr = 0;
  }

  $scope.endInscription = function() {
    $scope.model.ci = 0;
  }

  $scope.changeRegistration = function() {
    $scope.model.cr = ($scope.model.cr + 1) % $scope.model.registrations.length;
    $scope.checkInscriptionPreconditions();

    console.log($scope.model.user);
    console.log($scope.model.offer);
    console.log($scope.model.laboralData);
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

  $scope.formatUserToView = function(user) {
    user.birthdate = new Date(user.birthdate);
    for (var i = 0; i < user.telephones.length; i++) {
      var t = user.telephones[i];
      if (t.type == 'movil') {
        $scope.model.telephones.movil = t.number;
      } else {
        $scope.model.telephones.telephone = t.number;
      }
    }
  }

  $scope.findUserData = function() {
    var uid = Login.getUserId();

    Student.findById(uid).then(function(student) {
      if (student != null) {
        $scope.model.student = student;
      }
    });

    Users.findUser(uid, function(user) {
      console.log(user);
      $scope.formatUserToView(user);
      $scope.model.user = user;
    }, function(err) {
      console.log(err);
    })

    Users.findMails(uid, function(mails) {
      console.log(mails);
      $scope.model.mails.emails = mails;
      if (mails.length > 0) {
        $scope.model.mails.email = mails[0].id;
      }
    }, function(error) {
      console.log(err);
    });

  }

  $scope.updateUserData = function() {
    var ok = $scope.checkUserData();

    if (!ok) {
      return;
    }

    // corrijo la info de los telefonos para el formato de la llamada.
    $scope.model.user['telephones'] = [];
    $scope.model.user.telephones.push({
      number:$scope.model.telephones.telephone,
      type:'residence'
    });
    $scope.model.user.telephones.push({
      number:$scope.model.telephones.movil,
      type:'movil'
    });


    Users.updateUser($scope.model.user, function(res) {
      console.log(res);
    }, function(err) {
      console.log(err);
    })
  }

  $scope.updateStudentData = function() {
    console.log('los datos del legajo son de solo lectura');
  }

  $scope.updateLaboralData = function() {
    console.log('aca se actualiza la info del usuario que solo pertenece a insercion laboral');
  }

  $scope.checkUserData = function() {
    var ok = true;

    var form = $scope.dataBasic;

    ok = ok && form.name.$valid;
    ok = ok && form.lastname.$valid;
    ok = ok && form.dni.$valid;
    ok = ok && form.student_number.$valid;
    ok = ok && form.birthdate.$valid;
    ok = ok && form.genre.$valid;
    ok = ok && form.residence_city.$valid;
    ok = ok && form.address.$valid;
    ok = ok && form.birth_city.$valid;
    ok = ok && form.country.$valid;

    // chequeo que los telefonos sean validos y que por lo menos haya uno.
    ok = ok && form.movil.$valid;
    ok = ok && form.telephone.$valid;
    ok = ok && ($scope.model.telephones.telephone != '' || $scope.model.telephones.movil != '');

    // chequeo que tenga un email seleccionado de contacto
    ok = ok && ($scope.model.mails.email != '');

    return ok;
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
    LaboralInsertion.findAllInscriptionsByUser(userId)
      .then(function(data) {
        $scope.model.inscriptionsData = data.inscriptions;
        /*
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
        }];*/
      }, function(err) {
        console.log(err);
      });
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
    $scope.model.laboralData.languages.push({
        name: $scope.languages[0],
        level: 'Básico'
      });
  }

  $scope.deleteLanguage = function(l) {
    var languages = $scope.model.laboralData.languages;
    var i = languages.indexOf(l);
    languages.splice(i,1);
  }

  $scope.status = {

  };


  $scope.initialize = function(){
    $scope.findUserData();
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

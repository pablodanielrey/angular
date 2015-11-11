angular
  .module('mainApp')
  .controller('InscriptionCtrl', InscriptionCtrl);

InscriptionCtrl.inject = ['$rootScope', '$scope', '$wamp', 'LaboralInsertion', 'Login', 'Users', 'Student', 'Notifications', 'Files']

function InscriptionCtrl($rootScope, $scope, $wamp, LaboralInsertion, Login, Users, Student, Notifications, Files) {

  $scope.degrees = [
    { degree:'Contador Público', assignatures:34 },
    { degree:'Licenciatura en Administración', assignatures:37 },
    { degree:'Licenciatura en Turismo', assignatures:28 },
    { degree:'Licenciatura en Economía', assignatures:35 },
    { degree:'Tecnicatura en Cooperativas', assignatures:19 }
  ];
  $scope.workTypes = ['Pasantía','Full-Time','Programa estudiantes avanzados y jovenes profesionales'];
  $scope.travel = [
    { label:'No', value: false },
    { label:'Sí', value: true }
  ];
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
      birthdate: null,
      photo: ''
    },


    showInscription: false,

    // inscripcion a ser subida al server.
    offer: {
      degree: $scope.degrees[0].degree,
      graduate: false,
      average1: 0.0,
      average2: 0.0,
      approved: 0,
      workType: $scope.workTypes[0],
      travel: $scope.travel[0].value,
      workExperience: false
    },

    // información general de inserción laboral
    laboralData: {
      id: '',
      accepted_conditions: false,
      cv: '',
      email: '',
      languages: []
    }

  };


  $scope.addPhoto = function(fileName, fileContent) {
    var cv = window.btoa(fileContent);
    Files.upload(null, fileName, cv).then(
        function(id) {
          console.log(id);
          $scope.model.user.photo = id;
          $scope.updateUserData();
        },
        function(err) {
          console.log(err);
          Notifications.message(err);
        }

    )
  }


  $scope.addCV = function(fileName, fileContent) {
    var cv = window.btoa(fileContent);
    Files.upload(null, fileName, cv).then(
        function(id) {
          console.log(id);
          $scope.model.laboralData.cv = id;
        },
        function(err) {
          console.log(err);
          Notifications.message(err);
        }

    )
  }


  $scope.$watch(function() { return $scope.model.offer.degree; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.offer.average1; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.offer.average2; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.offer.approved; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  //$scope.$watch(function() { return $scope.model.laboralData.languages; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.laboralData.email; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.laboralData.cv; }, function(o,n) { $scope.checkInscriptionPreconditions(); });

  $scope.checkInscriptionPreconditions = function() {

      var ok = true;
      var offer = $scope.model.offer;

      if ($scope.model.cr >= 0) {

        ok = false;
        for (var i = 0; i < $scope.degrees.length; i++) {
          if (offer.degree == $scope.degrees[i].degree) {
            ok = true;
            if (offer.graduate) {
              offer.approved = $scope.degrees[i].assignatures;
            }
            break;
          }
        }

      }

      if ($scope.model.cr >= 1) {

        /*
          condiciones:
            los promedios estan entre 0 y 10
            la cantidad de materias aprobadas va de 0 a (dependiendo de la carrera la cantidad de materias)
            la cantidad de materias aprobadas deben superar el 80% de la cantidad de materias de la carrera
        */

        ok = ok && offer.average1 >= 0;
        if (offer.average1 > 10) {
          offer.average1 = 10;
        } else if (offer.average1 <= 0) {
          offer.average1 = 0;
        }

        ok = ok && offer.average2 >= 0;
        if (offer.average2 > 10) {
          offer.average2 = 10;
        } else if (offer.average2 <= 0) {
          offer.average2 = 0;
        }

        for (var i = 0; i < $scope.degrees.length; i++) {
          if (offer.degree == $scope.degrees[i].degree) {
            var assignatures = $scope.degrees[i].assignatures;
            if (offer.approved > assignatures) {
              offer.approved = assignatures;
              break;
            }
            // controlo que tenga aprobado el 80%
            var minimum = (assignatures * 80) / 100;
            if (offer.approved > minimum) {
              $scope.workTypes = ['Full-Time','Programa estudiantes avanzados y jovenes profesionales'];
            } else {
              $scope.workTypes = ['Pasantía','Full-Time'];
            }
            offer.workType = $scope.workTypes[0];

            if (offer.approved <= 0) {
              offer.approved = 0;
            }

            break;
          }
        }

      }

      if ($scope.model.cr >= 3) {
          if (offer.travel == undefined || offer.travel == '') {
            ok = false;
          }
      }

      if ($scope.model.cr >= 4) {

        var languages = $scope.model.laboralData.languages
        for (var l = 0; l < languages.length; l++) {
          for (var i = l + 1; i < languages.length; i++) {
            if (languages[l].name == languages[i].name) {
              ok = false;
            }
          }
        }
      }


      if ($scope.model.cr >= 5) {
        ok = ok && ($scope.model.laboralData.cv != null && $scope.model.laboralData.cv != '');
      }

      console.log(ok);
      $scope.model.showNext = ok;
    }

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

    $scope.checkInscriptionPreconditions();
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
    $scope.checkInscriptionPreconditions();
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
    $scope.model.laboralData.id = uid;

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
        $scope.model.laboralData.email = mails[0].id;
      }
    }, function(err) {
      console.log(err);
    });


    LaboralInsertion.findByUser(uid).then(
      function(laboralData) {
        if (laboralData == null) {
          return;
        }
        console.log(laboralData);
        $scope.model.laboralData = laboralData;
      },
      function(err) {
        console.log(err);
      }
    );

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
    var ld = JSON.parse(JSON.stringify($scope.model.laboralData))
    if (ld.cv == undefined || ld.cv == '') {
      delete ld.cv;
    }
    LaboralInsertion.persist(ld).then(null,function(err) {console.log(err)});
  }

  $scope.checkUserData = function() {

    /*
      Se cheqeuan que los datos del formulario sean validos con respecto a las expresiones regulares seteaas en el formulario.
      condiciones:

    */

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

    var userId = Login.getUserId();

    //// ESTO SE ELIMINA TODOOO //////
    var ld = JSON.parse(JSON.stringify($scope.model.laboralData))
    if (ld.cv == undefined || ld.cv == '') {
      delete ld.cv;
    }
    ////////

    console.log($scope.model.offer);

    Promise.all([
      LaboralInsertion.persist(ld),
      LaboralInsertion.persistInscriptionByUser(userId, $scope.model.offer)]
    ).then(function(v,v) {
      $scope.getInscriptions();
    }, function(err) {
      console.log(err);
    });
  }

  $scope.getInscriptions = function() {
    var userId = Login.getUserId();
    LaboralInsertion.findAllInscriptionsByUser(userId)
      .then(function(data) {
        $scope.model.inscriptionsData = data;
      }, function(err) {
        console.log(err);
      });
  }

  $scope.getDegree = function(i) {
    return i.degree;
  }

  $scope.getType = function(i) {
    return i.workType;
  }

  $scope.downloadInscription = function(i) {
    console.log(i);
  }

  $scope.removeInscription = function(i) {
    LaboralInsertion.deleteInscriptionById(i.id).then(
      function() {
        $scope.getInscriptions();
      }, function(err) {
        console.log(err);
      }
    );
  }


  $scope.addLanguage = function() {

    /*
      Se controla que los lenguajes existan solo una vez en la lista de lenguajes.
      al agregar uno, se selecciona automáticamente el primero que no este ya agregado a la lista.
    */

    var lang = '';
    for (var l = 0; l < $scope.languages.length; l++) {
      lang = $scope.languages[l];
      for (var i = 0; i < $scope.model.laboralData.languages.length; i++) {
        var lang2 = $scope.model.laboralData.languages[i].name;
        if (lang2 == lang) {
          lang = '';
          break;
        }
      }
      if (lang != '') {
        break;
      }
    }

    if (lang == '') {
      return;
    }

    $scope.model.laboralData.languages.push({
        name: lang,
        level: 'Básico'
      });
  }

  $scope.deleteLanguage = function(l) {
    var languages = $scope.model.laboralData.languages;
    var i = languages.indexOf(l);
    languages.splice(i,1);
    $scope.checkInscriptionPreconditions();
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

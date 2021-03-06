angular
  .module('mainApp')
  .controller('InscriptionCtrl', InscriptionCtrl);

InscriptionCtrl.inject = ['$rootScope', '$scope', '$timeout', '$wamp', 'LaboralInsertion', 'Login', 'Users', 'Student', 'Notifications', 'Files']

function InscriptionCtrl($rootScope, $scope, $timeout, $wamp, LaboralInsertion, Login, Users, Student, Notifications, Files) {

  $scope.boolToStr = function(arg) {
    if (arg == null) {
      return 'Seleccionar';
    }
    return arg ? 'Sí' : 'No'
  };

  $scope.degrees = [
    { degree:'Seleccionar' },
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
    finish: false,
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
    telephoneRequired:true,

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

    loadingPhoto: false,
    formatPhoto: false,             // error de formato de la foto
    loadingCv: false,
    formatCV: false,                // error de formato del cv
    showInscription: false,

    // inscripcion a ser subida al server.
    offer: {
      degree: null,
      graduate: false,
      average1: 0.0,
      average2: 0.0,
      approved: 0,
      workType: null,
      travel: null,
      workExperience: null
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

  $scope.view = {
    styleIsMessage: '',
    styleMessage: '',
    error: []
  }

  $scope.getUserPhoto = function() {
    if ($scope.model.user.photo == null || $scope.model.user.photo == '') {
      return null;
    } else {
      return "/c/files.py?i=" + $scope.model.user.photo;
    }
  }


  $scope.addPhoto = function(fileName, fileContent) {

    $scope.model.formatPhoto = false;
    console.log(fileName);

    re = /^.*\.jpg$/i
    if (!re.test(fileName)) {
      console.log('formato no soportado');
      $scope.model.formatPhoto = true;
      return;
    }

    $scope.model.loadingPhoto = true;

    var photo = window.btoa(fileContent);
    Files.upload(null, fileName, 'image/jpeg', Files.BASE64, photo).then(
        function(id) {
          $scope.model.loadingPhoto = false;
          $scope.model.user.photo = id;
          $scope.updateUserData();
        },
        function(err) {
          $scope.model.loadingPhoto = false;
          console.log(err);
          Notifications.message(err);
        }

    )
  }


  $scope.addCV = function(fileName, fileContent) {

    $scope.model.formatCV = false;

    re = /^.*\.pdf$/i
    if (!re.test(fileName)) {
      // console.log('formato no soportado');
      $scope.model.formatCV = true;
      return;
    }

    $scope.model.loadingCv = true;

    var cv = window.btoa(fileContent);
    Files.upload(null, fileName, 'application/pdf', Files.BASE64, cv).then(
        function(id) {
          $scope.model.cv_name = fileName;
          $scope.model.loadingCv = false;
          $scope.model.laboralData.cv = id;
        },
        function(err) {
          $scope.model.loadingCv = false;
          console.log(err);
          Notifications.message(err);
          $scope.model.laboralData.cv = null;
          $scope.model.formatCV = true;
        }

    )
  }

  function changeApproved() {
    var offer = $scope.model.offer;
    offer.approved = 0;
    if (offer.degree == null || offer.degree == 'Seleccionar') {
      return;
    }
    if (offer.graduate) {
      for (var i = 0; i < $scope.degrees.length; i++) {
        if (offer.degree == $scope.degrees[i].degree) {
          offer.approved = $scope.degrees[i].assignatures;
          return;
        }
      }
    }
  }

  $scope.$watch(function() { return $scope.model.offer.degree; }, function(o,n) { $scope.checkInscriptionPreconditions(); changeApproved()});
  $scope.$watch(function() { return $scope.model.offer.average1; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.offer.average2; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.offer.approved; }, function(o,n) {$scope.checkInscriptionPreconditions();});
  $scope.$watch(function() { return $scope.model.offer.graduate; }, function(o,n) {
    changeApproved();
  });
  //$scope.$watch(function() { return $scope.model.laboralData.languages; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.laboralData.email; }, function(o,n) { $scope.checkInscriptionPreconditions(); });
  $scope.$watch(function() { return $scope.model.laboralData.cv; }, function(o,n) { $scope.checkInscriptionPreconditions(); });

  $scope.$watch(function() {return $scope.model.telephones.telephone;}, function(o,n) {
    $scope.model.telephoneRequired = ($scope.model.telephones.movil == null ||$scope.model.telephones.movil == "") &&
                                     ($scope.model.telephones.telephone == null || $scope.model.telephones.telephone == "");
  });


  $scope.$watch(function() {return $scope.model.telephones.movil;}, function(o,n) {
    $scope.model.telephoneRequired = ($scope.model.telephones.movil == null ||$scope.model.telephones.movil == "") &&
                                     ($scope.model.telephones.telephone == null || $scope.model.telephones.telephone == "");
  });

  $scope.$watch(function() { return $scope.model.mails.emails;}, function(o,n) {
    if ($scope.model.mails == null || $scope.model.mails.emails == null || $scope.model.mails.emails.length <= 0) {
      return
    }
    if ($scope.model.laboralData.email == null || $scope.model.laboralData.email == "") {
      $scope.model.selectedEmail = $scope.model.mails.emails[0];
      $scope.updateLaboralData();
    } else {
      for (var i = 0; i < $scope.model.mails.emails.length; i++) {
        var m = $scope.model.mails.emails[i];
        if ($scope.model.laboralData.email == m.id) {
          $scope.model.selectedEmail = m;
          break;
        }
      }
    }

  });

  $scope.checkInscriptionPreconditions = function() {

      var ok = true;
      var offer = $scope.model.offer;
      if ($scope.model.cr == 0) {
        if (offer.degree == null || offer.degree == 'Seleccionar') {
          ok = false;
        } else {
          ok = false;
          for (var i = 0; i < $scope.degrees.length; i++) {
            if (offer.degree == $scope.degrees[i].degree) {
              ok = true;
              break;
            }
          }
        }

        offer.average1 = 0;
        offer.average2 = 0;
      }

      if ($scope.model.cr == 1) {

        /*
          condiciones:
            los promedios estan entre 0 y 10
            la cantidad de materias aprobadas va de 0 a (dependiendo de la carrera la cantidad de materias)
        */

        if (offer.average1 > 10) {
          offer.average1 = 10;
        } else if (offer.average1 <= 0) {
          offer.average1 = 0;
        }
        ok = ok && offer.average1 > 0;

        if (offer.average2 > 10) {
          offer.average2 = 10;
        } else if (offer.average2 <= 0) {
          offer.average2 = 0;
        }
        ok = ok && offer.average2 > 0;

        if (offer.average2 > offer.average1) {
          offer.average2 = offer.average1;
        }

        var assignatures = 0;
        for (var i = 0; i < $scope.degrees.length; i++) {
          if (offer.degree == $scope.degrees[i].degree) {
            assignatures = $scope.degrees[i].assignatures;
            break;
          }
        }

        if (offer.approved > assignatures) {
          offer.approved = assignatures;
        }

        if (offer.approved <= 0) {
          offer.approved = 0;
        }

        // controlo que tenga aprobado el 80%
        var minimum = (assignatures * 80) / 100;
        if (offer.approved == assignatures) {
          $scope.workTypes = ['Seleccionar', 'Full-Time','Programa estudiantes avanzados y jovenes profesionales'];
        } else if (offer.approved > minimum) {
          $scope.workTypes = ['Seleccionar', 'Pasantía','Full-Time','Programa estudiantes avanzados y jovenes profesionales'];
        } else {
          $scope.workTypes = ['Seleccionar', 'Pasantía','Full-Time'];
        }
        //offer.workType = $scope.workTypes[0];
        offer.workType = 'Seleccionar';
        offer.workExperience = null;

      }

      if ($scope.model.cr == 2) {
        offer.travel = null;

        ok = (offer.workType != 'Seleccionar');
        ok = ok && (offer.workExperience != null);
      }

      if ($scope.model.cr == 3) {
          ok = (offer.travel != null);
      }

      if ($scope.model.cr == 4) {

        // me fijo solo que no haya repetidos
        var languages = $scope.model.laboralData.languages
        for (var l = 0; l < languages.length; l++) {
          for (var i = l + 1; i < languages.length; i++) {
            if (languages[l].name == languages[i].name) {
              ok = false;
              break;
            }
          }
        }

      }

      if ($scope.model.cr == 5) {
        ok = ($scope.model.laboralData.cv != null && $scope.model.laboralData.cv != '');
      }

      $scope.model.showNext = ok;
    }

  // --- elementos graficos -----

  $scope.model.totalPages = $scope.model.registrations.length;

  $scope.startInscription = function() {
    $scope.model.finish = false;
    var ok = $scope.checkUserData();
    if (!ok) {
      $scope.view.styleIsMessage = 'mensajes';
      $scope.view.styleMessage = 'msjError';
      return;
    }

    $scope.model.ci = 1;
    $scope.model.cr = 0;

    $scope.model.offer.degree = 'Seleccionar';

    $scope.checkInscriptionPreconditions();
  }

  $scope.closeMessage = function() {
    $scope.view.styleIsMessage = '';
    $scope.view.styleMessage = '';
  }

  $scope.endInscription = function() {
    $scope.model.ci = 0;
  }

  $scope.changeRegistration = function() {
    $scope.model.cr = ($scope.model.cr + 1) % $scope.model.registrations.length;
    $scope.checkInscriptionPreconditions();
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
    var uid = $scope.userId;
    $scope.model.laboralData.id = uid;

    Student.findById(uid).then(function(student) {
      if (student != null) {
        $scope.model.student = student;
      }
    });

    Users.findById([uid])
      .then(function(users) {
        if (users != null && users.length > 0) {
          $scope.formatUserToView(users[0]);
          $scope.model.user = users[0];
        }
      }, function(err) {
          console.log(err);
    });

    Users.findMails(uid, function(mails) {
      $scope.model.mails.emails = mails;
    }, function(err) {
      console.log(err);
    });


    LaboralInsertion.findByUser(uid).then(
      function(laboralData) {
        if (laboralData == null) {
          return;
        }
        $scope.model.laboralData = laboralData;

        // encuentro los metadatos del cv si es que esta cargado
        if (laboralData.cv != undefined && laboralData.cv != null) {
          Files.findMetaDataById(laboralData.cv).then(
            function(data) {
              $scope.model.cv_name = data.name;
            },
            function(err) {
              console.log(err);
            }
          );
        }

      },
      function(err) {
        console.log(err);
      }
    );

  }

  $scope.updateUserData = function() {
    //var ok = $scope.checkUserData();

    //if (!ok) {
    //  console.log('faltan datos requeridos')
    //  return;
    //}

    // corrijo la info de los telefonos para el formato de la llamada.
    $scope.model.user['telephones'] = [];

    if ($scope.model.telephones.telephone != null && $scope.model.telephones.telephone.trim() != "") {
      $scope.model.user.telephones.push({
        number: $scope.model.telephones.telephone,
        type: 'residence'
      });
    }

    if ($scope.model.telephones.movil != null && $scope.model.telephones.movil.trim() != "") {
      $scope.model.user.telephones.push({
        number: $scope.model.telephones.movil,
        type: 'movil'
      });
    }

    Users.updateUser($scope.model.user, function(res) {

    }, function(err) {
      console.log(err);
    })
  }

  $scope.updateStudentData = function() {
    // console.log('los datos del legajo son de solo lectura');
  }

  $scope.updateLaboralData = function() {
    $scope.model.laboralData.emailId = $scope.model.selectedEmail == null ? null : $scope.model.selectedEmail.id;
    var ld = JSON.parse(JSON.stringify($scope.model.laboralData))
    if (ld.cv == undefined || ld.cv == '') {
      delete ld.cv;
    }
    console.log(ld);
    LaboralInsertion.persist(ld).then(null,function(err) {console.log(err)});
  }

  $scope.checkUserData = function() {

    /*
      Se cheqeuan que los datos del formulario sean validos con respecto a las expresiones regulares seteaas en el formulario.
      condiciones:

    */

    var ok = true;
    $scope.view.error = [];

    var form = $scope.dataBasic;

    if (!form.name.$valid) {
      $scope.view.error.push("Debe ingresar su nombre");
    }
    ok = ok && form.name.$valid;

    if (!form.lastname.$valid) {
      $scope.view.error.push("Debe ingresar su apellido");
    }
    ok = ok && form.lastname.$valid;

    if (!form.dni.$valid) {
      $scope.view.error.push("Número de documento incorrecto");
    }
    ok = ok && form.dni.$valid;

    if (!form.student_number.$valid) {
      $scope.view.error.push("Número de legajo incorrecto");
    }
    ok = ok && form.student_number.$valid;

    if (!form.birthdate.$valid) {
      $scope.view.error.push("Debe seleccionar un fecha de nacimiento");
    }
    ok = ok && form.birthdate.$valid;

    if (!form.genre.$valid) {
      $scope.view.error.push("Debe seleccionar el género");
    }
    ok = ok && form.genre.$valid;

    if (!form.residence_city.$valid) {
      $scope.view.error.push("Debe ingresar la ciudad de residencia");
    }
    ok = ok && form.residence_city.$valid;

    if (!form.address.$valid) {
      $scope.view.error.push("Debe ingresar la dirección");
    }
    ok = ok && form.address.$valid;

    if (!form.birth_city.$valid) {
      $scope.view.error.push("Debe ingresar la ciudad de nacimiento");
    }
    ok = ok && form.birth_city.$valid;

    if (!form.country.$valid) {
      $scope.view.error.push("El país ingresado es incorrecto");
    }
    ok = ok && form.country.$valid;

    // chequeo que los telefonos sean validos y que por lo menos haya uno.
    ok = ok && form.movil.$valid;
    ok = ok && form.telephone.$valid;

    var validTel = ($scope.model.telephones.telephone != '' || $scope.model.telephones.movil != '');
    if (!validTel || !form.movil.$valid || !form.telephone.$valid) {
      $scope.view.error.push("Debe ingresar al menos un teléfono");
    }
    ok = ok && validTel;

    // chequeo que tenga un email seleccionado de contacto
    if ($scope.model.selectedEmail == null) {
      $scope.view.error.push("Debe seleccionar un e-mail");
    }
    ok = ok && ($scope.model.selectedEmail != null);

    return ok;
  }


  $scope.uploadInscription = function() {

    var userId = $scope.userId;


    //// ESTO SE ELIMINA TODOOO //////
    var ld = JSON.parse(JSON.stringify($scope.model.laboralData))
    if (ld.cv == undefined || ld.cv == '') {
      delete ld.cv;
    }
    ////////

    Promise.all([
      LaboralInsertion.persist(ld),
      LaboralInsertion.persistInscriptionByUser(userId, $scope.model.offer)]
    ).then(function(v,v) {
      $scope.changeRegistration();
      $scope.model.finish = true;
      $scope.$apply();
    }, function(err) {
      console.log(err);
    });
  }

  $scope.finishInscription = function() {
    $scope.endInscription();
    $scope.getInscriptions();
  }

  function filterDeleted(inscriptions) {
    var active = Array();
    for (var i = 0; i < inscriptions.length; i++) {
      if (!inscriptions[i].deleted) {
        active.push(inscriptions[i]);
      }
    }
    return active;
  }

  $scope.getInscriptions = function() {
    var userId = $scope.userId;
    LaboralInsertion.findAllInscriptionsByUser(userId)
      .then(function(data) {
        var data2 = filterDeleted(data)
        $scope.model.inscriptionsData = data2;
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
    // console.log(i);
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
    $scope.userId = '';
    Login.getSessionData()
      .then(function(s) {
          $scope.userId = s.user_id;
          $scope.initialize();
      }, function(err) {
        console.log(err);
      });
  });



};

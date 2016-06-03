angular
  .module('mainApp')
  .controller('HomeCtrl', HomeCtrl);

HomeCtrl.inject = ['$rootScope', '$scope', 'Account', 'Login', 'Users', 'Student', '$timeout']

function HomeCtrl($rootScope, $scope, Account, Login, Users, Student, $timeout) {

  $scope.initialize = initialize;
  $scope.search = search;
  $scope.loadUser = loadUser;
  $scope.viewSearch = viewSearch;
  $scope.createUser = createUser;
  $scope.save = save;
  $scope.updateType = updateType;
  $scope.getType = getType;
  $scope.getMailEcono = getMailEcono;
  $scope.getMailAlternative = getMailAlternative;
  $scope.deleteMail = deleteMail;
  $scope.toMail = toMail;
  $scope.getStudentNumber = getStudentNumber;

  $scope.model = {
      search: '',
      user: null,
      student: null,
      mails: [],
      types: [],
      allTypes: [{value:'student', description:'Alumno'}, {value:'teacher', description:'Profesor'},
                {value:'postgraduate', description:'Posgrado'}, {value:'graduate', description:'Graduado'},
                {value:'assistance', description:'No docente'}],
      selectedType: null
  }

  $scope.view = {
    style: 'pantallaBusqueda',
    styles: ['pantallaBusqueda', 'pantallaUsuarioNoExiste', 'pantallaCrearUsuario', 'pantallaUsuarioCreado',
             'pantallaInfoDeUsuario', 'pantallaMailEliminado', 'pantallaCargando', 'pantallaError']
  }

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.model.userId = '';
    Login.getSessionData()
      .then(function(s) {
          $scope.model.userId = s.user_id;
          $scope.initialize();
      }, function(err) {
        console.log(err);
      });
  });

  function initialize() {
    $scope.view.style = $scope.view.styles[0];
    $scope.model.types = [];
    Account.getTypes().then(function(types) {
      for (var i = 0; i < types.length; i++) {
        for (var j = 0; j < $scope.model.allTypes.length; j++) {
          if (types[i] == $scope.model.allTypes[j].value) {
            $scope.model.types.push($scope.model.allTypes[j]);
          }
        }
      }
    }, function(err) {
      console.log(err);
    });
  }

  function loadUser(user) {
    uid = user.id;
    $scope.model.user = user;
    $scope.view.style = $scope.view.styles[4];

    $scope.model.selectedType = null;
    for (var i = 0; i < $scope.model.allTypes.length; i++) {
      if (user.type == $scope.model.allTypes[i].value) {
        $scope.model.selectedType = $scope.model.allTypes[i];
        break;
      }
    }

    $scope.model.mails = [];
    Users.findAllMails(uid).then(function(mails) {
      $scope.model.mails = mails;
    }, function(error) {
      console.log(error);
    });

    $scope.model.student = null;

    Student.findById(uid).then(function(student) {
      if (student == null) {
        $scope.model.student = null;
        return;
      }
      $scope.model.student = student;
    }, function(error) {
      console.log(error);
    });
  }

  function search() {
    if ($scope.model.search == '') {
      return
    }
    $scope.view.style = $scope.view.styles[6];
    Account.findByDni($scope.model.search).then(function(users) {
      if (users == null || users.length <= 0) {
        $scope.model.user = {};
        $scope.$apply(function() {
          $scope.view.style = $scope.view.styles[1];
        });
        return;
      }
      $scope.loadUser(users[0]);
    }, function(error) {
      $scope.$apply(function() {
        $scope.view.style = $scope.view.styles[7];
      });
      console.log(error);
    });

  }

  function viewSearch() {
    $scope.model.search = "";
    $scope.view.style = $scope.view.styles[0];
  }

  function createUser() {
    $scope.view.style = $scope.view.styles[2];
    $scope.model.user = {};
    $scope.model.user.dni = $scope.model.search;
    $scope.model.student = {studentNumber:''};
    $scope.model.mails = [];
    $scope.model.selectedType = $scope.model.types[0];
  }

  function verifyCreate() {
    if ($scope.model.user.name == '') {
      return false
    }
    if ($scope.model.user.lastname == '') {
      return false
    }
    if ($scope.model.user.dni == '') {
      return false
    }

    if ($scope.model.selectedType.value == 'student' && $scope.model.student.studentNumber == '') {
      return false
    }
    return true;
  }

  function updateType() {
    Account.updateType($scope.model.user, $scope.model.selectedType.value).then(function(data) {
      console.log("Se modifico correctamente");
      alert("Se modificó correctamente");
    }, function(error) {
      console.log(error);

    });
  }

  function save() {
    if (!verifyCreate()) {
      return;
    }

    Account.createUser($scope.model.user, $scope.model.student, $scope.model.selectedType).then(function(data) {
      $scope.view.style = $scope.view.styles[3];
    }, function(error) {
      console.log(error);
      $scope.view.style = $scope.view.styles[7];
      $timeout(function () {
        $scope.view.style = $scope.view.styles[2];
      }, 2000);
    });

  }

  function getType() {
    if ($scope.model.user == null || $scope.model.user.type == null) {
      return "No posee";
    }
    for (var i = 0; i < $scope.model.types.length; i++) {
      var t = $scope.model.types[i];
      if (t.value == $scope.model.user.type) {
        return t.description;
      }
    }
    return "No posee";
  }

  function getMailEcono() {
    if ($scope.model.user == null || $scope.model.mails == null) {
      return null;
    }
    for (var i = 0; i < $scope.model.mails.length; i++) {
      m = $scope.model.mails[i];
      if (m.email.indexOf('@econo.unlp.edu.ar') > -1) {
        return m;
      }
    }
    return null;
  }

  function getMailAlternative() {
    if ($scope.model.user == null || $scope.model.mails == null) {
      return null;
    }
    for (var i = 0; i < $scope.model.mails.length; i++) {
      m = $scope.model.mails[i];
      if (m.email.indexOf('@econo.unlp.edu.ar') <= -1) {
        return m;
      }
    }
    return null;
  }

  function deleteMail() {
    mail = $scope.getMailAlternative();
    if (mail == null) {
      return;
    }
    Account.deleteMail(mail.id).then(function(data) {
      $scope.view.style = $scope.view.styles[5];
    }, function(error) {
      console.log(error);
      $scope.view.style = $scope.view.styles[7];
      $timeout(function () {
        $scope.view.style = $scope.view.styles[1];
      }, 2000);
    });
  }

  function toMail(mail) {
    return (mail == null) ? "No posee" : mail.email;
  }

  function getStudentNumber() {
    return ($scope.model.student == null) ? "No posee" : $scope.model.student.studentNumber;
  }


}

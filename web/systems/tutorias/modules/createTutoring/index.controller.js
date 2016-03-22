angular
  .module('mainApp')
  .controller('CreateTutoringCtrl',CreateTutoringCtrl);

CreateTutoringCtrl.inject = ['$rootScope', '$scope', 'Login', 'Users', 'Tutors', '$timeout'];

function CreateTutoringCtrl($rootScope, $scope, Login, Users, Tutors, $timeout) {

  $scope.model = {
    tutoring: {
      id: null,
      tutorId: '',
      tutor: {},
      date: new Date(),
      situations: []        // arreglo de objetos del tipo {user: {user:{}, student:{}}, situation: ''}
    },
    searchResults: [],
    searching: false,
    search: '',
    tutorings: [],
    recentUsers: [],
    situations: ['Situación académica','Situación económica','Situación personal']
  }

  $scope.view = {
    style: '',
    style2: ''
  }


  $scope.initializeNewTutoring = function(date) {
    $scope.model.tutoring = {
          id: null,
          tutorId: '',
          tutor: {},
          date: date,
          situations: []        // arreglo de objetos del tipo {user: {user:{}, student:{}}, situation: ''}
        };
    }

  $scope.delete = function(tid) {
    Tutors.delete(tid)
      .then(function(ok) {

        $scope.initialize();
        $scope.view.style = '';
        $scope.view.style2 = '';

      }, function(err) {
        cosole.log(err);
      })
  }

  $scope.createNewTutoring = function() {
    $scope.initializeNewTutoring($scope.model.tutoring.date);

    Login.getSessionData()
      .then(function(s) {
          var userId = s.user_id;
          Users.findById([userId])
            .then(function(users) {
                var user = users[0];
                user.img = 'img/avatarMen.jpg';
                $scope.model.tutoring.tutor = user;
                $scope.model.tutoring.tutorId = userId;
            }, function(err) {
                console.log(err);
            });
      }, function(err) {
        console.log(err);
      });

    $scope.view.style = 'nuevaTutoria';
  }

  $scope.deleteStudent = function(user) {
    var i = $scope.findByDniInSituations(user, $scope.model.tutoring.situations);
    $scope.model.tutoring.situations.splice(i,1);
  }


  $scope.findByDni = function(user, userList) {
    var dni = user['user'].dni;
    for (var i = 0; i < userList.length; i++) {
      if (userList[i]['user'].dni == dni) {
        return i;
      }
    }
    return -1;
  }

  $scope.findByDniInSituations = function(user, situationList) {
    var dni = user['user'].dni;
    for (var i = 0; i < situationList.length; i++) {
      if (situationList[i].user['user'].dni == dni) {
        return i;
      }
    }
    return -1;
  }

  $scope.addStudent = function(user) {
    var i = $scope.findByDni(user, $scope.model.searchResults);
    if (i >= 0) {
      $scope.model.searchResults.splice(i,1);
    }

    i = $scope.findByDni(user, $scope.model.recentUsers);
    if (i < 0) {
      $scope.model.recentUsers.push(user);
    }

    i = $scope.findByDni(user, $scope.model.tutoring.situations);
    if (i < 0) {
      var situation = {
        user: user,
        situation: $scope.model.situations[0]
      };
      $scope.model.tutoring.situations.push(situation);
    }
    $scope.view.style2='';
  }

  $scope.searchStudents = function() {

    if ($scope.model.searching) {
      console.log('buscando');
      return;
    }

    if ($scope.model.search == '') {
      $scope.view.style2='';
      return;
    }

    $scope.model.searching = true;
    $scope.view.style2 = 'verResultados';
    $scope.searchResults = [];
    $scope.view.style3 = 'cargandoBusqueda';

    Tutors.search($scope.model.search)
    .then(function(users) {
      $scope.$apply(function() {
        $scope.view.style3 = '';
        $scope.model.searching = false;
        $scope.model.searchResults = users
      });
    }, function(err) {
      $scope.view.style3 = '';
      $scope.model.searching = false;
      console.log(err);
    })

    console.log('ejecutado')
  }

  $scope.initialize = function() {
    $scope.loadTutorings();
    //$scope.loadRecentUsers();
  }

  $scope.loadTutorings = function() {
    $scope.model.tutorings = [];
    Tutors.loadTutorings()
    .then(function(tutorings) {
      // $scope.model.tutorings.push({'date':'26/03/2016','day':'Martes'});
      $scope.$apply(function() {
        $scope.model.tutorings = tutorings;
      });
    }, function(err) {
      console.log(err);
    });
  }

  $scope.loadRecentUsers = function() {
    $scope.model.recentUsers = [];
    $scope.model.recentUsers.push({'img':'img/pablosarmieto.jpg','name':'Pablo','lastname':'Sarmiento','dni':'30235968'});
    $scope.model.recentUsers.push({'img':'img/lucas.jpg','name':'Lucas','lastname':'Langoni','dni':'35456923'});
    $scope.model.recentUsers.push({'img':'img/walter.jpg','name':'Walter','lastname':'Blanco','dni':'30001823'});
    $scope.model.recentUsers.push({'img':'img/pablo.jpg','name':'Pablo Daniel','lastname':'Rey','dni':'28356952'});
  }

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });


  $scope.selectTutoring = function(t) {
    $scope.view.style = 'nuevaTutoria';
    $scope.model.tutoring = t;
  }

  $scope.save = function() {

    // acomodo el id del tutor y elimino los datos del tutor asi no transfiero tanto hacia el servidor.
    $scope.model.tutoring.tutorId = $scope.model.tutoring.tutor.id;
    $scope.model.tutoring.tutor = null;

    // acomodo las situaciones para que tengan el userId correctamente.
    // y elimino los datos del usuario para no enviar datos la santo botón al servidor.
    for (var i = 0; i < $scope.model.tutoring.situations.length; i++) {
      $scope.model.tutoring.situations[i].userId = $scope.model.tutoring.situations[i].user.user.id;
      $scope.model.tutoring.situations[i].user = null;
    }

    Tutors.persist($scope.model.tutoring)
    .then(function(id) {
        $scope.initializeNewTutoring(new Date());
        $scope.view.style3='mensajes';
        $scope.view.style4='msjGuardada';
        $scope.loadTutorings();

        $timeout(function () {
          $scope.view.style = '';
          $scope.view.style3 = '';
        }, 3000);

    }, function(err) {
      console.log('error');
    });

  }

  $scope.cancel = function() {
    $scope.view.style3='mensajes';
    $scope.view.style4='msjCancelada';
  }

  $scope.back = function() {
    $scope.view.style3 = '';
  }

  $scope.confirmCancel = function() {
    $scope.view.style = '';
    $scope.view.style3 = '';
  }

}

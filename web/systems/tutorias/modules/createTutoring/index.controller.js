angular
  .module('mainApp')
  .controller('CreateTutoringCtrl',CreateTutoringCtrl);

CreateTutoringCtrl.inject = ['$rootScope', '$scope', 'Login', 'Tutors', '$timeout'];

function CreateTutoringCtrl($rootScope, $scope, Login, Tutors, $timeout) {

  $scope.model = {
    tutoring: {
      search: '',
      tutor: {},
      date: new Date(),
      participants: []
    },
    tutorings: [],
    recentUsers: []
  }

  $scope.view = {
    style: '',
    style2: ''
  }


  $scope.createNewTutoring = function() {
    $scope.model.tutoring.participants = [
        // {name:'Pablo Rey', img: 'img/pablo.jpg', dni: '27294557'}
    ];

    Login.getSessionData()
    .then(function(s) {
      $scope.$apply([
        $scope.model.tutoring.tutor = {
          name: s.login.username,
          img: ''
        }
      ]);
    }, function(err) {
      $scope.$apply([
        $scope.model.tutoring.tutor = {
          name: 'Error',
          img: ''
        }
      ]);
    });

    $scope.view.style = 'nuevaTutoria';
  }

  $scope.deleteParticipant = function(user) {
    $scope.model.tutoring.participants.splice($scope.model.tutoring.participants.indexOf(user),1);
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

  $scope.addParticipant = function(user) {
    var i = $scope.findByDni(user, $scope.model.searchResults);
    if (i >= 0) {
      $scope.model.searchResults.splice(i,1);
    }

    i = $scope.findByDni(user, $scope.model.recentUsers);
    if (i < 0) {
      $scope.model.recentUsers.push(user);
    }

    i = $scope.findByDni(user, $scope.model.tutoring.participants);
    if (i < 0) {
      $scope.model.tutoring.participants.push(user);
    }
    $scope.view.style2='';
  }

  $scope.searchParticipants = function() {

    if ($scope.model.searching) {
      console.log('buscando');
      return;
    }

    if ($scope.model.search == '') {
      $scope.view.style2='';
      return;
    }

    if ($scope.model.search.length < 3) {
      console.log('Muy pocos caracteres. como mínimo deben ser 3');
      return;
    }

    $scope.model.searching = true;
    $scope.view.style2='verResultados';
    $scope.searchResults = [];

    Tutors.search($scope.model.search)
    .then(function(users) {
      $scope.model.searching = false;
      $scope.model.searchResults = users
    }, function(err) {
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
        $scope.model.tutorings = tutorings;
    }, function(err) {

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
  }

  $scope.save = function() {
    Tutors.persist(tutoring)
    .then(function(data) {
      $scope.view.style3='mensajes';
      $scope.view.style4='msjGuardada';
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

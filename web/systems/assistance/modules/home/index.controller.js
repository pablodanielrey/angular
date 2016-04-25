angular
  .module('mainApp')
  .controller('HomeCtrl', HomeCtrl);

HomeCtrl.inject = ['$rootScope', '$scope', 'Users', 'Login', 'Positions', 'Assistance']

function HomeCtrl($rootScope, $scope, Users, Login, Positions, Assistance) {

  $scope.initialize = initialize;
  $scope.loadUser = loadUser;
  $scope.getUserPhoto = getUserPhoto;
  $scope.loadPosition = loadPosition;
  $scope.loadAssistanceData = loadAssistanceData;

  $scope.model = {
    user: null,
    userId: '',
    date : new Date()
  }

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

  $scope.$watch(function() {return $scope.model.date;}, function(o,n) {
    $scope.loadAssistanceData();
  });

  function initialize() {
    $scope.model.date = new Date();
    $scope.loadUser();
    $scope.loadPosition();
    $scope.loadAssistanceData();
  }

  function loadPosition() {
    Positions.getPosition([$scope.userId]).then(function(positions) {
      $scope.model.position = (positions.length > 0) ? positions[0] : null;
    }, function(error) {
      console.log('Error al buscar el cargo')
    });
  }

  function loadUser() {
    Users.findById([$scope.userId]).then(function(users) {
      $scope.model.user = (users.length > 0) ? users[0] : null;
    }, function(error) {
      console.log('Error al buscar el usuario')
    });
  }

  function getUserPhoto() {
    if ($scope.model.user == null || $scope.model.user.photo == null || $scope.model.user.photo == '') {
      return "../login/modules/img/imgUser.jpg";
    } else {
      return "/c/files.py?i=" + $scope.model.user.photo;
    }
  }

  function loadAssistanceData() {
    if ($scope.model.date == null || $scope.userId == null) {
      return
    }
    Assistance.getAssistanceData([$scope.userId], $scope.model.date, $scope.model.date).then(function(data) {
      console.log(data);
    }, function(error) {
      console.log("Error al obtener los datos de asistencia");
    })
  }


}

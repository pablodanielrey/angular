angular
  .module('mainApp')
  .controller('HomeCtrl', HomeCtrl);

HomeCtrl.inject = ['$rootScope', '$scope', 'Users', 'Login']

function HomeCtrl($rootScope, $scope, Users, Login) {

  $scope.initialize = initialize;
  $scope.loadUser = loadUser;

  $scope.model = {
    user: null,
    userId: ''
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

  function initialize() {
    $scope.loadUser();
  }

  function loadUser() {
    Users.findById([$scope.userId]).then(function(users) {
      $scope.model.user = (users.length > 0) ? users[0] : null;
    }, function(error) {
      console.log('Error al buscar el usuario')
    });
  }


}

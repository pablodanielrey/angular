angular
  .module('mainApp')
  .controller('PasswordCtrl', PasswordCtrl);

PasswordCtrl.inject = ['$rootScope', '$scope', 'Systems', 'Login', '$timeout']

function PasswordCtrl($rootScope, $scope, Systems, Login, $timeout) {

  $scope.initialize = initialize;
  $scope.changePassword = changePassword;
  $scope.checkPassword = checkPassword;

  $scope.model = {
    userId: '',
    password: '',
    passwrod2: '',
    passwordOk: false
  }

  $scope.view = {
    style: 'ocultarMensajes',
    styleOptions: ['ocultarMensajes', 'avisoCargando', 'avisoError', 'avisoPassDistintos', 'avisoErrorPass', 'avisoOk']
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
    $scope.view.style = $scope.view.styleOptions[0];
    $scope.model.password = '';
    $scope.model.password2 = '';
  }

  function checkPassword() {
    $scope.model.passwordOk = false;

    if ($scope.model.password.length > 5) {
      if ($scope.model.password == $scope.model.password2) {
        return true;
      }
      $scope.view.style = $scope.view.styleOptions[3];
      return false;
    }
    $scope.view.style = $scope.view.styleOptions[4];
    return false;
  }

  function changePassword() {
    $scope.view.style = $scope.view.styleOptions[0];
    if (!$scope.checkPassword()) {
      return;
    }

    Systems.changePassword($scope.model.password).then(
        function(data) {
          $scope.$apply(function() {
            $scope.view.style = $scope.view.styleOptions[5];
            $timeout(function () {
              $scope.initialize();
            }, 3000);
          });
        },
        function(err) {
          $scope.$apply(function() {
            $scope.view.style = $scope.view.styleOptions[2];
          });
        }
    )
  }

}

angular
  .module('mainApp')
  .controller('ResetPasswordCtrl', ResetPasswordCtrl);

ResetPasswordCtrl.$inject = ['$rootScope','$scope', '$wamp', '$window'];

function ResetPasswordCtrl($rootScope, $scope, $wamp, $window) {

    $scope.model = {
      screens: ["pantallaDNI", "pantallaCodigo", "pantallaContrasena", "pantallaFin", "pantallaSinCorreoAlternativo", "pantallaSinCorreoAlternativo"],
      errors: ["", "noExisteDNI", "errorDeCodigo", "errorDeContrasena"],
      clazzScreen: "pantallaDNI",
      clazzError: "",
      dni: "",
      email: "",
      code: "",
      pass1: "",
      pass2: "",
      userData: null
    }

    $scope.requestDni = function() {
      $scope.model.clazzError = $scope.model.errors[0];
      $scope.model.clazzScreen = $scope.model.screens[0];
    };

    $scope.requestNoMail = function() {
      $scope.model.clazzError = $scope.model.errors[0];
      $scope.model.clazzScreen = $scope.model.screens[5];
    }

    $scope.requestCode = function() {
      $scope.model.clazzError = $scope.model.errors[0];
      $scope.model.clazzScreen = $scope.model.screens[1];
    };

    $scope.requestPassword = function() {
      $scope.model.clazzError = $scope.model.errors[0];
      $scope.model.clazzScreen = $scope.model.screens[2];
    }

    $scope.finalize = function() {
      $scope.model.clazzScreen = $scope.model.screens[3];
    }

    $scope.finish = function() {
      $window.location.href = '/';
    }

    $scope.processDni = function() {
      $wamp.call('system.login.findByDni', [$scope.model.dni]).then(
        function(userData) {
          console.log(userData);
          if (userData == null) {
            $scope.model.clazzError = $scope.model.errors[1];
            return;
          } else {
            if (userData[1] == null) {
              $scope.requestNoMail();
              return;
            } else {
              $scope.model.userData = userData;
              $scope.model.email = String.copy(userData[1].email).replace(/(....).*@(.*)/,'$1*****@$2');
              $scope.requestCode();
              return;
            }
          }
        },
        function(err) {
          $scope.model.clazzError = $scope.model.errors[1];
        }
      )
    }

    $scope.processCode = function() {
      var email = $scope.model.userData[1];
      $wamp.call('system.login.checkCode', [email.id, $scope.model.code]).then(
        function(ok) {
          if (ok) {
            $scope.requestPassword();
          } else {
            console.log(ok);
            $scope.model.clazzError = $scope.model.errors[2];
          }
        },
        function(err) {
          console.log(err);
          $scope.model.clazzError = $scope.model.errors[2];
        }
      );
    }

    $scope.processPassword = function() {

      if ($scope.model.pass1 != $scope.model.pass2) {
        $scope.model.clazzError = $scope.model.errors[3];
        return;
      }

      var user = $scope.model.userData[0];
      var email = $scope.model.userData[1];
      $wamp.call('system.login.changePassword', [user.id, user.dni, email.id, $scope.model.code, $scope.model.pass1]).then(
        function(ok) {
          if (ok) {
            $scope.finalize();
          } else {
            console.log(ok);
          }
        },
        function(err) {
          console.log(err);
        }
      );
    }


    $rootScope.loaded = false;
    $scope.loaded = false;

    $rootScope.$on("$wamp.open", function (event, session) {
      $scope.$broadcast('wampOpenEvent', event);
    });

    $rootScope.$on("$wamp.close", function (event, session) {
      $scope.$broadcast('wampCloseEvent',event);
    });

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.requestDni();
    });

};

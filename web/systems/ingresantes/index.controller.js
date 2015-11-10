
app.controller('IngresantesCtrl',IngresantesCtrl);

IngresantesCtrl.$inject = ['$rootScope','$scope', '$window', 'Notifications', 'Users', 'Student', '$wamp'];

function IngresantesCtrl($rootScope, $scope, $window, Notifications, Users, Student, $wamp) {

    $scope.screens = ['home','genero','mail', 'activacion', 'password', 'fin'];
    $scope.errors = ['', 'DNInoExiste', 'DNIActivado', 'CorreoNoLlega', 'consultaEnviada', 'mostrarEspere'];

    $scope.model = {
      si: 0,
      se: 0,
      screen: $scope.screens[0] + ' ' + $scope.errors[0],
      user: null,
      gender: {
        male: false,
        female: false,
        nd: false
      },
      email: {
        id: '',
        email: '',
        code: '',
        invalid: false,
        sending: false,
        times: 0
      },

      dniOk: false,
      dni: '',

      password: '',
      password2: '',
      passwordVisible: false,
      passwordOk: false,

      error: {
        names:'',
        dni:'',
        email:'',
        tel:''
      }
    };

    $scope.setMale = function() {
      $scope.model.gender.nd = false;
      $scope.model.gender.female = false;
      $scope.model.user.genre = 'Masculino';
    }

    $scope.setFemale = function() {
      $scope.model.gender.nd = false;
      $scope.model.gender.male = false;
      $scope.model.user.genre = 'Femenino';
    }

    $scope.setNd = function() {
      $scope.model.gender.male = false;
      $scope.model.gender.female = false;
      $scope.model.user.genre = 'Otro';
    }

    $scope.setGender = function() {
      //if ($scope.model.gender.male || $scope.model.gender.female || $scope.model.gender.nd) {
        $scope.changeScreen();
      //}
    }

    $scope.getClazz = function() {
      /*
      <!--CLASES (home, genero, mail,activacion, password,fin)  y (mostrarEspere, ocultarEspere) y de errores (DNInoExiste, DNIActivado, CorreoNoLlega, consultaEnviada )-->
      */
      $scope.model.screen = $scope.screens[$scope.model.si] + ' ' + $scope.errors[$scope.model.se];
      return $scope.model.screen;
    }


    $scope.checkDniSyntax = function() {
      console.log('checkDniSyntax');
      $scope.model.dniOk = false;
      var re = /^\d{8,8}$/i;
      $scope.model.dniOk = re.test($scope.model.dni);
    }

    // pasos de la aplicación
    $scope.checkDni = function() {
      var dni = $scope.model.dni;
      Users.findByDni(dni).then(
        function(user) {
          if (user == null) {
            $scope.model.se = 1;
            return;
          }
          console.log(user);
          $scope.model.user = user;

          //chequeo a ver si tiene ya mails activos
          Users.findAllMails(user.id).then(
            function(mails) {
              if (mails == null || mails.length <= 0) {
                // no tiene emails. por lo que esta perfecto. paso de pantalla
                $scope.changeScreen();
                return;
              }

              var i = 0;
              for (i = 0; i < mails.length; i++) {
                var m = mails[i];
                if (m.confirmed) {
                  $scope.model.se = 2;
                  console.log(m);
                  return;
                }
              }

              // no existe ningun mail validado.
              $scope.changeScreen();
            },
            function(err) {
              console.log(err);
            }
          );

        },
        function(err) {
          console.log(err);
        }
      );
    }

    $scope.sendEmailValidation = function() {
      var oemail = {
        user_id: $scope.model.user.id,
        email: $scope.model.email.email
      };
      Users.persistMail(oemail).then(
        function(eid) {
          $scope.model.email.id = eid;
          $scope.resendEmailValidation();
          $scope.changeScreen();
        },
        function(err) {
          console.log(err);
        }
      );
    }

    $scope.resendEmailValidation = function() {
      if ($scope.model.email.times >= 4) {
        $scope.model.se = 3;  // CorreoNoLlega
        return;
      }
      $scope.model.email.times = $scope.model.email.times + 1;

      $scope.model.email.invalid = false;
      $scope.model.email.code = '';

      $scope.model.email.sending = true;
      $wamp.call('ingreso.mails.sendEmailConfirmation', [$scope.model.user.name, $scope.model.user.lastname, $scope.model.email.id]).then(
        function(ok) {
          $scope.model.email.sending = false;
        },
        function(err) {
          console.log(err);
          $scope.model.email.sending = false;
        }
      );
    }

    $scope.checkEmailCode = function() {
      $scope.model.email.invalid = false;
      $wamp.call('ingreso.mails.confirmEmail', [$scope.model.email.id, $scope.model.email.code]).then(
        function(ok) {
          if (!ok) {
            $scope.model.email.invalid = true;
          } else {
            $scope.changeScreen();
          }
        },
        function(err) {
          console.log(err);
        }
      );
    }

    $scope.checkPassword = function() {
      $scope.model.passwordOk = false;
      var re = /^([a-zA-Z]+\d+)+[a-zA-Z]*$/i;

      if (re.test($scope.model.password)) {
        $scope.model.passwordOk = ($scope.model.password == $scope.model.password2);
      }
    }

    $scope.changePassword = function() {
      $wamp.call('ingreso.user.changePassword', [$scope.model.dni, $scope.model.password]).then(
        function(ok) {
          var pass = '';
          if (!ok) {
            // TODO: falta poner que ya tiene una clave seteada.
            console.log(ok);
            pass = 'Ya tenía una existente. puede restablecerla entrando en www.fce.econo.unlp.edu.ar';
          } else {
            pass = $scope.model.password;
          }

          $scope.changeScreen();
          $scope.model.se = 5;

          $wamp.call('ingreso.mails.sendFinalMail',[$scope.model.user, pass, $scope.model.email.email]).then(
            function(ok) {
              $scope.model.se = 0;
            },
            function(err) {
              console.log(err);
              $scope.model.se = 0;
            }
          );

        },
        function(err) {
          console.log(err);
        }
      );
    }


    $scope.changeScreen = function() {
      var sc = $scope.screens;
      $scope.model.si = $scope.model.si + 1 % sc.length;
      $scope.getClazz();
    }

    $scope.changeScreenBackwards = function() {
      var sc = $scope.screens;
      $scope.model.si = $scope.model.si - 1 % sc.length;
      $scope.getClazz();
    }


    // errores e informes

    $scope.wrongDni = function() {
      $scope.model.se = 5;
      var error = $scope.model.error;
      $wamp.call('ingreso.mails.sendErrorMail',['DNI inexistente', error.names, error.dni, error.email, error.tel]).then(
        function(ok) {
          $scope.model.se = 4;
        },
        function(err) {
          console.log(err);
        }
      );
    }

    $scope.alreadyActive = function() {
      $scope.model.se = 5;
      var error = $scope.model.error;
      $wamp.call('ingreso.mails.sendErrorMail',['Ya tiene cuenta', error.names, error.dni, error.email, error.tel]).then(
        function(ok) {
          $scope.model.se = 4;
        },
        function(err) {
          console.log(err);
        }
      );
    }

    $scope.noCode = function() {
      $scope.model.se = 5;
      var error = $scope.model.error;
      $wamp.call('ingreso.mails.sendErrorMail',['No llega el código', error.names, error.dni, error.email, error.tel]).then(
        function(ok) {
          $scope.model.se = 4;
        },
        function(err) {
          console.log(err);
        }
      );
    }



    $scope.initialize = function() {
      console.log('inicializando');
    }

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });

};

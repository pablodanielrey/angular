
app.controller('IngresantesCtrl',IngresantesCtrl);

IngresantesCtrl.$inject = ['$rootScope','$scope', '$window', 'Notifications', 'Users', 'Student'];

function IngresantesCtrl($rootScope, $scope, $window, Notifications, Users, Student) {

    $scope.screens = ['home','genero','mail', 'activacion', 'password', 'fin'];
    $scope.errors = ['', 'DNInoExiste', 'DNIActivado', 'CorreoNoLlega'];

    $scope.model = {
      si: 0,
      se: 0,
      screen: $scope.screens[0] + ' ' + $scope.errors[0],
      dni: ''
    };



    $scope.getClazz = function() {
      /*
      <!--CLASES (home, genero, mail,activacion, password,fin)  y (mostrarEspere, ocultarEspere) y de errores (DNInoExiste, DNIActivado, CorreoNoLlega, consultaEnviada )-->
      */
      $scope.model.screen = $scope.screens[$scope.model.si] + ' ' + $scope.errors[$scope.model.se];
      return $scope.model.screen;
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
          $scope.changeScreen();
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





    $scope.initialize = function() {
      console.log('inicializando');
    }

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });

};

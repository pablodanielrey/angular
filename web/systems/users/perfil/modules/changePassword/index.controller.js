 (function() {
    'use strict';

    angular
        .module('users')
        .controller('ChangePasswordCtrl', ChangePasswordCtrl);

    ChangePasswordCtrl.$inject = ['$scope', '$timeout', '$q', '$location', 'Users', 'Utils', 'Login'];


    function ChangePasswordCtrl($scope, $timeout, $q, $location, Users, Utils,  Login) {

      //Inicializar componente
      var init = function(){
        $scope.component = {
          disabled: true, //flag para indicar si el formulario esta deshabilitado o no
          message: "Iniciando", //mensaje
          userId: null //Identificacion de la entidad que esta siendo administrada
        };

      };

      var initUser = function(){
        $scope.component.userId = Login.getCredentials()["userId"]
        $scope.component.message = null;
        $scope.component.disabled = false;
      }



      //Enviar formulario
      $scope.sendCode = function(){
        $scope.component.disabled = true;
        $scope.component.message = "Enviando Codigo";

          var p = Utils.findAlternativeAndConfirmedEmail($scope.component.userId).then(
            function(email){

              if(!email) {
                $scope.component.message = "ERROR: No existen emails alternativos confirmados"
                $scope.$apply();
                return false;
              }
            }
        );
      }

      //Inicializar
      init();
      $timeout(initUser, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

    }
})();

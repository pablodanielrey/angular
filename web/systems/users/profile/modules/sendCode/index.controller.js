 (function() {
    'use strict';

    angular
        .module('users.profile')
        .controller('SendCodeCtrl', SendCodeCtrl);

    SendCodeCtrl.$inject = ['$scope', '$timeout', '$q', '$location', 'UsersProfile', 'Login'];


    function SendCodeCtrl($scope, $timeout, $q, $location, UsersProfile, Login) {

      //Inicializar componente
      var init = function(){
        $scope.component = {
          disabled: true, //flag para indicar si el formulario esta deshabilitado o no
          message: "Iniciando", //mensaje
          userId: null, //Identificacion de la entidad que esta siendo administrada
          error: false  //flag para indicar error
        };

      };

      var initUser = function(){
        $scope.component.userId = Login.getCredentials()["userId"]

        var urlParams = $location.search();
        if("id" in urlParams) {
          $scope.emailId = urlParams["id"];
        } else {
          return;
        }

        $scope.component.message = null;
        $scope.component.disabled = false;
      }

      //Enviar formulario
      $scope.sendCode = function(){
        $scope.component.disabled = true;
        $scope.component.message = "Enviando Codigo";

        UsersProfile.sendEmailConfirmation($scope.component.userId, $scope.emailId).then(
          function(response) {
            $timeout(function() {
              $location.path( "/setCode/" + $scope.emailId);
            });

          }, function (error) {
            $scope.component.message = "Error";
            $scope.component.error = true;
          }
        );
      }

      //Inicializar
      init();
      $timeout(initUser, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

    }
})();

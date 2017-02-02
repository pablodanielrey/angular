 (function() {
    'use strict';

    angular
        .module('users.recover')
        .controller('ChangePasswordSetCodeCtrl', ChangePasswordSetCodeCtrl);

    ChangePasswordSetCodeCtrl.$inject = ['$scope', '$timeout', '$q', '$location', 'UsersRecover', 'Login'];


    function ChangePasswordSetCodeCtrl($scope, $timeout, $q, $location, UsersRecover, Login) {

      //Inicializar componente
      $scope.component = {
        disabled: true, //flag para indicar si el formulario esta deshabilitado o no
        message: "Iniciando", //mensaje
        error: false, //flag para indicar que existio un error
      };

      var init = function(){
        var urlParams = $location.search();
        if("id" in urlParams) $scope.userId = urlParams["id"];
        $scope.component.message = null;
        $scope.component.disabled = false;
      }

      //Enviar formulario
      $scope.submit = function(){
        $scope.component.disabled = true;
        $scope.component.message = "Procesando";

        UsersRecover.processCode($scope.code).then(
          function(response){
            if(!response) {
              $scope.component.message = "Error";
              $scope.component.error = true;
            } else {
              $location.path( "/changePassword");
            }
          }
        )
      }




      //Inicializar
      init();
      $timeout(init, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

    }
})();

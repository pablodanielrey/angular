(function() {
  'use strict';

  angular.module('users.recover').controller('IdentificateCtrl', IdentificateCtrl);
    IdentificateCtrl.$inject = ['$scope', '$timeout', '$q', '$location', 'UsersRecover', 'Login'];

    function IdentificateCtrl($scope, $timeout, $q, $location, UsersRecover, Login) {

      //Inicializar componente
      $scope.component = { disabled: true, message: "Iniciando", error: false };

      var init = function(){
        $scope.dni = null;
        $scope.component.message = null;
        $scope.component.disabled = false;
      }


     //Enviar formulario
     $scope.submit = function(){
       $scope.component.disabled = true;
       $scope.component.message = "Procesando";

       if(!$scope.dni) {
         $scope.component.disabled = false;
         $scope.component.message = "No puede estar vacio";
         return;
      }

       UsersRecover.sendCodeByDni($scope.dni).then(
         function(user){
           if(!user){
             $scope.component.message = "Usuario no identificado";
             return
           } else {
             $location.path("/changePasswordSetCode");
             $scope.$apply()

           }
         },
         function(error){
           alert("error");
           console.log(error)
         }
       )
     }

     //Inicializar
     $timeout(init, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

   }
})();

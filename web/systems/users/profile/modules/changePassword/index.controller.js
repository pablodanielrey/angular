(function() {
   'use strict';

   angular
       .module('users.profile')
       .controller('ChangePasswordCtrl', ChangePasswordCtrl);

   ChangePasswordCtrl.$inject = ['$scope', '$timeout', '$q', '$location', 'UsersProfile', 'Login'];


   function ChangePasswordCtrl($scope, $timeout, $q, $location, UsersProfile, Login) {

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
       $scope.component.message = null;
       $scope.component.disabled = false;
     }


     //Enviar formulario
     $scope.submit = function(){
       $scope.component.disabled = true;
       $scope.component.message = "Procesando";

       UsersProfile.changePassword($scope.password).then(
         function(response){
           if(!response) {
             $scope.component.message = "Error";
             $scope.component.error = true;
           } else {
             $location.path( "/changePasswordSuccess");
           }
         }
       )
     }

     //Inicializar
     init();
     $timeout(initUser, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

   }
})();
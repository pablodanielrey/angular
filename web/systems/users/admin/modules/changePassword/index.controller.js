(function() {
   'use strict';

   angular
       .module('users.admin')
       .controller('ChangePasswordCtrl', ChangePasswordCtrl);

   ChangePasswordCtrl.$inject = ['$scope', '$timeout', '$q', '$location', 'UsersAdmin', 'Login'];


   function ChangePasswordCtrl($scope, $timeout, $q, $location, UsersAdmin, Login) {

     //Inicializar componente

     $scope.component = {
       disabled: true, //flag para indicar si el formulario esta deshabilitado o no
       message: "Iniciando", //mensaje
       error: false  //flag para indicar error
     };

     $scope.userId = null;
     $scope.password = null;
     $scope.password2 = null;

     var init = function(){
       var urlParams = $location.search();
       if("id" in urlParams)  $scope.userId = urlParams["id"];

       $scope.component.message = null;
       $scope.component.disabled = false;
     }


     //Enviar formulario
     $scope.submit = function(){
       $scope.component.disabled = true;
       $scope.component.message = "Procesando";

       if($scope.password != $scope.password2) {
         $scope.component.message = "Las claves no coinciden";
         $scope.component.disabled = false;
         return;
       }

       UsersAdmin.changePassword($scope.userId, $scope.password).then(
         function(response){
           console.log(response)
           $scope.component.message = "Guardado"
           $scope.$apply()
         },
         function(error){
           alert("error");
           console.log(error)
         }
       )
     }

     $scope.back = function() {
       window.history.back();
     }

     //Inicializar
     $timeout(init, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

   }
})();

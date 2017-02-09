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
       $scope.alerts = [];
     };

     var initUser = function(){
       $scope.component.userId = Login.getCredentials()["userId"]
       $scope.component.message = null;
       $scope.component.disabled = false;
       $scope.code = '';
       $scope.code2 = '';
     }

     $scope.closeAlert = function(index) {
       $scope.alerts.splice(index, 1);
     }

     $scope.closeAllAlerts = function() {
       $scope.alerts = [];
     }

     //Enviar formulario
     $scope.submit = function(){
       $scope.closeAllAlerts();
       if (!validate()) {
         return;
       }

       $scope.component.disabled = true;
       $scope.component.message = "Procesando";

       UsersProfile.changePassword($scope.code).then(
         function(response){
             $scope.alerts.push({type: 'success', msg: 'Los cambios se han guardado correctamente'});
             $scope.$apply();
             return;
           if(!response) {
             $scope.component.message = "Error";
             $scope.component.error = true;
           } else {
             $location.path( "/changePasswordSuccess");
           }
         }, function(error) {
           $scope.alerts.push({type: 'danger', title: 'Error: ' + error.error, msg:  error.args[0]})
           $scope.$apply();
         }
       )
     }

     function validate() {
       $scope.code = $scope.code.trim();
       $scope.code2 = $scope.code2.trim();

       if ($scope.code == '') {
         $scope.alerts.push({type: 'danger', title: 'Error: clave vacía', msg:  'Ingrese la clave nuevamente'})
         return false;
       }

       if ($scope.code.length < 6) {
         $scope.alerts.push({type: 'danger', title: 'Error: no cumple con los requisitos', msg:  'Ingrese la clave nuevamente'})
         return false;
       }

       if ($scope.code != $scope.code2) {
         $scope.alerts.push({type: 'danger', title: 'Error: las claves no coinciden', msg:  'Ingrese la clave nuevamente'})
         return false;
       }

       return true;

     }

     //Inicializar
     init();
     $timeout(initUser, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

   }
})();

 (function() {
    'use strict';

    angular
        .module('users.admin')
        .controller('ListEmailsCtrl', ListEmailsCtrl);

    ListEmailsCtrl.$inject = ['$scope', '$timeout', '$location', '$uibModal', 'UsersAdmin'];


    function ListEmailsCtrl($scope, $timeout, $location, $uibModal, UsersAdmin) {

      //Inicializar componente
      function init(){
        $scope.alerts = [];
        $scope.component = {
          disabled: true, //flag para indicar si el formulario esta deshabilitado o no
          message: "Inicializando", //mensaje
          userId: null //Identificacion del usuario que esta siendo administrado
        };

        var urlParams = $location.search();
        if("id" in urlParams) $scope.component.userId = urlParams["id"];
      };

      function initUser(){
          UsersAdmin.findEmailsByUserId($scope.component.userId).then(
            function(emails){
              $scope.component.message = null
              $scope.emails = emails;
              $scope.$apply();
            },
            function(error){
              $scope.alerts.push({type: 'danger', title: 'Error al buscar los correos del usuario ', msg:  error.args[0]})
              $scope.$apply();
            }
          )
      }

      $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
      }

      $scope.closeAllAlerts = function() {
        $scope.alerts = [];
      }

      //Open modal add email
      $scope.addEmail = function () {
        var d = new Date();
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: "modules/addEmail/index.html?d="+d.getTime(),
          controller: "AddEmailCtrl",
          resolve: {
            userId: function () { return $scope.component.userId; }
          }
        });

        modalInstance.result.then(
           function (email) {
             $scope.emails.push(email);
             $scope.alerts.push({type: 'success', title: "Correo agregado",msg: 'Se ha creado el siguiente correo: ' + email.email});
           }, function (error) {
             $scope.alerts.push({type: 'danger', title: 'Error al crear el correo ', msg:  error.args[0]})
           }
         );
       };

       $scope.sendConfirmation = function(email) {
         UsersAdmin.sendConfirmation($scope.component.userId, email.id).then(
           function (result) {
             $scope.alerts.push({type: 'success', title: "Confirmacion enviada",msg: 'Se ha enviado un correo con el código a la dirección: ' + email.email});
             $scope.$apply();
           }, function(error) {
             $scope.alerts.push({type: 'danger', title: 'Error al enviar la confirmación ', msg:  error.args[0]})
             $scope.$apply();

           }
         )
       }

       $scope.deleteEmail = function(index){
         UsersAdmin.deleteEmail($scope.emails[index]).then(
           function(email){
             var e = $scope.emails[index].email;
             $scope.emails.splice(index, 1);
             $scope.alerts.push({type: 'success', title: "Correo eliminado",msg: 'El correo ' + e + ' ha sido eliminado'});
             $scope.$apply();
           },
           function(error){
             $scope.alerts.push({type: 'danger', title: 'Error al eliminar el correo ', msg:  error.args[0]})
             $scope.$apply();
           }
         )
       }


      $scope.confirmEmail = function(index) {
         $scope.component.message = "Confirmando"
         UsersAdmin.persistEmail($scope.emails[index]).then(
           function(email){
             if (email.confirmed) {
               $scope.alerts.push({type: 'success', title: "Cambio de estado exitoso",msg: 'El correo ' + email.email + ' ha sido confirmado'});
             } else {
               $scope.alerts.push({type: 'success', title: "Cambio de estado exitoso",msg: 'El estado del correo ' + email.email + ' es pendiente de confirmación'});
             }

             $scope.$apply();

           },
           function(error){
             $scope.alerts.push({type: 'danger', title: 'Error al confirmar el correo ', msg:  error.args[0]})
             $scope.$apply();
           }
         )
      }

      $scope.back = function() {
        window.history.back();
      }


      init();
      $timeout(initUser, 500); //TODO reemplazar $timeout por algun evento que indique inicializacion

    }
})();

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
              $scope.component.disabled = false;
              $scope.component.message = null
              $scope.emails = emails;
              $scope.$apply();
            },
            function(error){
               alert("error");
               console.log(error);
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
           }, function (error) {
               console.log(error);
           }
         );
       };

       $scope.sendConfirmation = function(email) {
         UsersAdmin.sendConfirmation($scope.component.userId, email.id).then(
           function (result) {
             $scope.alerts.push({type: 'success', title: "Confirmacion enviada",msg: 'Se ha enviado un correo con el código a la dirección: ' + email.email});
             $scope.$apply();
           }, function(error) {
             $scope.alerts.push({type: 'danger', title: 'Error: al enviar la confirmación ', msg:  error.args[0]})
             $scope.$apply();

           }
         )
       }

       $scope.deleteEmail = function(index){
         UsersAdmin.deleteEmail($scope.emails[index]).then(
           function(email){
             $scope.emails.splice(index, 1);
             $scope.$apply();
           },
           function(error){
              alert("error")
              console.log(error);
           }
         )
       }


      $scope.confirmEmail = function(index){
         $scope.component.disabled = true
         $scope.component.message = "Confirmando"
         UsersAdmin.persistEmail($scope.emails[index]).then(
           function(email){
             $scope.component.disabled = false;
             $scope.component.message = "Email Confirmado";
             $scope.$apply();

           },
           function(error){
              alert("error")
              console.log(error);
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

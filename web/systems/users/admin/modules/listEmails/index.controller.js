 (function() {
    'use strict';

    angular
        .module('users.admin')
        .controller('ListEmailsCtrl', ListEmailsCtrl);

    ListEmailsCtrl.$inject = ['$scope', '$timeout', '$location', '$uibModal', 'UsersAdmin'];


    function ListEmailsCtrl($scope, $timeout, $location, $uibModal, UsersAdmin) {

      //Inicializar componente
      function init(){
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

      //Open modal add email
      $scope.addEmail = function () {
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: "modules/addEmail/index.html",
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



      init();
      $timeout(initUser, 500); //TODO reemplazar $timeout por algun evento que indique inicializacion

    }
})();

 (function() {
    'use strict';

    angular
        .module('users')
        .controller('ListEmailsCtrl', ListEmailsCtrl);

    ListEmailsCtrl.$inject = ['$scope', '$timeout', '$location', '$uibModal', 'Users', 'Login'];


    function ListEmailsCtrl($scope, $timeout, $location, $uibModal, Users, Login) {

      //Inicializar componente
      function init(){
        $scope.component = {
          disabled: true, //flag para indicar si el formulario esta deshabilitado o no
          message: "Inicializando", //mensaje
          userId: null //Identificacion del usuario que esta siendo administrado
        };

        $scope.component.userId = Login.getCredentials()["userId"]

      };

      function initUser(){
        var p = Users.findByIds([$scope.component.userId]).then(
          function(users){ $scope.user = users[0]; },
          function(error){
             alert("error")
             console.log(error)
          }
        )

        p.then(
          Users.findEmailsByUserId($scope.component.userId).then(
            function(emails){
              $scope.emails = emails;
              console.log($scope.emails);
              $scope.$apply();
            },
            function(error){
               alert("error")

            }
          )

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
         Users.deleteEmail($scope.emails[index]).then(
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




      init();
      $timeout(initUser, 500); //TODO reemplazar $timeout por algun evento que indique inicializacion

    }
})();

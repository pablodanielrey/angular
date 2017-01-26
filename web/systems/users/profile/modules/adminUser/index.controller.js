 (function() {
    'use strict';

    angular
        .module('users.profile')
        .controller('AdminUserCtrl', AdminUserCtrl);

    AdminUserCtrl.$inject = ['$scope', '$timeout', '$q', '$location', 'UsersProfile', 'Login'];


    function AdminUserCtrl($scope, $timeout, $q, $location, UsersProfile, Login) {

      $scope.form = {
        disabled: true, //flag para indicar si el formulario esta deshabilitado o no
        message: "Inicializando", //mensaje
        id: null //Identificacion de la entidad que esta siendo administrada
      };

      $scope.form.id = Login.getCredentials()["userId"]


      //Inicializar usuario
      var initUser = function(){

        UsersProfile.findById($scope.form.id).then(
          function(user){
            $scope.user = user;
            $scope.form.disabled = false;
            $scope.form.message = null;
            $scope.$apply();
            console.log(user)

          },
          function(error){
             alert("error")
             console.log(error)
          }
        )
      }

      //Enviar formulario
      $scope.submit = function(){
        $scope.form.disabled = true;
        $scope.form.message = "Procesando";

        UsersProfile.persist($scope.user).then(
          function(response){
            $scope.form.message = "Guardado";
            $scope.$apply();
          },
          function(error){
             alert("error")
             console.log(error)
          }
        )
      }

      //Agregar / eliminar telefono
      $scope.addTelephone = function() { $scope.user.telephones.push({__json_class__:"Telephone", __json_module__
:"model.users.entities.user", number:null, type:null}) };
      $scope.deleteTelephone = function(index){ $scope.user.telephones.splice(index, 1); }; //Eliminar telefono



      //Inicializar
      $timeout(initUser, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

    }
})();

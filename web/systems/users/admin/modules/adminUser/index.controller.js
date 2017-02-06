 (function() {
    'use strict';

    angular
        .module('users.admin')
        .controller('AdminUserCtrl', AdminUserCtrl);

    AdminUserCtrl.$inject = ['$scope', '$timeout', '$q', '$location', 'UsersAdmin'];


    function AdminUserCtrl($scope, $timeout, $q, $location, UsersAdmin) {

      //Inicializar componente
      var init = function(){
        $scope.form = {
          disabled: true, //flag para indicar si el formulario esta deshabilitado o no
          message: "Inicializando", //mensaje
          id: null //Identificacion de la entidad que esta siendo administrada
        };

        var urlParams = $location.search();
        if("id" in urlParams) {
          $scope.form.id = urlParams["id"];
          $scope.action = 'edit';
        } else {
          $scope.action = 'create';
        }
      };

      //Inicializar usuario
      var initUser = function(){
        UsersAdmin.admin($scope.form.id).then(
          function(user){
            console.log(user)
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

        console.log($scope.user);
        UsersAdmin.persist($scope.user).then(
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

      $scope.back = function() {
        window.history.back();
      }

      //Agregar / eliminar telefono
      $scope.addTelephone = function() { $scope.user.telephones.push({__json_class__:"Telephone", __json_module__
:"model.users.entities.user", number:null, type:null}) };
      $scope.deleteTelephone = function(index){ $scope.user.telephones.splice(index, 1); }; //Eliminar telefono

      //Agregar / eliminar tipo
      $scope.addType = function() { $scope.user.types.push({description:null}) };
      $scope.deleteType = function(index){ $scope.user.types.splice(index, 1); };

      //Inicializar
      init();
      $timeout(initUser, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

    }
})();

 (function() {
    'use strict';

    angular
        .module('users')
        .controller('AdminUserCtrl', AdminUserCtrl);

    AdminUserCtrl.$inject = ['$scope', '$timeout', '$q', '$location', 'Users'];


    function AdminUserCtrl($scope, $timeout, $q, $location, Users) {


      //Inicializar variables del formulario
      var initForm = function(){
        $scope.form = {
          disabled: true, //flag para indicar si el formulario esta deshabilitado o no
          message: "Inicializando", //mensaje
          id: null //Identificacion de la entidad que esta siendo administrada
        };
      };

      //Inicializar parametros.
      //Si existe el parametro "id" se realiza una busqueda en la base de datos y se cargan los valores.
      var initParams = function(){
        var urlParams = $location.search();
        if("id" in urlParams) $scope.form.id = urlParams["id"];
      };

      //inicializar fields
      var initFields = function(){
        Users.admin($scope.form.id).then(
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

      $scope.submit = function(){
        $scope.form.disabled = true;
        $scope.form.message = "Procesando";

        Users.persist($scope.user).then(
          function(response){
            console.log(response)
            $scope.form.message = "Guardado";
            $scope.$apply();
          },
          function(error){
             alert("error")
             console.log(error)
          }
        )
      }

      //Agregar telefono
      $scope.addTelephone = function() { $scope.user.telephones.push({__json_class__:"Telephone", __json_module__
:"model.users.entities.user", number:null, type:null}) };

      //Eliminar telefono
      $scope.deleteTelephone = function(index){ $scope.user.telephones.splice(index, 1); };

      initForm();
      initParams();
      $timeout(initFields, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

    }
})();

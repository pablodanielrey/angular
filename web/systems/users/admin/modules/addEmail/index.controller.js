 (function() {
    'use strict';

    angular
        .module('users')
        .controller('AddEmailCtrl', AddEmailCtrl);

    AddEmailCtrl.$inject = ['$scope', '$uibModalInstance', 'Users', 'userId'];

    function AddEmailCtrl($scope, $uibModalInstance, Users, userId) {


      //Inicializar componente
      var init = function(){
        $scope.form = {
          disabled: false, //flag para indicar si el formulario esta deshabilitado o no
          message: null, //mensaje
          userId: userId //Identificacion de la entidad que esta siendo administrada
        };

        $scope.email = {
          __json_class__:"Mail",
          __json_module__:"model.users.entities.mail",
          userId: userId,
          email:null,
          confirmed:false,
          hash:null
        }
      };


      //Enviar formulario
      $scope.submit = function(){
        $scope.form.disabled = true;
        $scope.form.message = "Procesando";

        Users.addEmail($scope.email).then(
          function(email){
            $scope.form.message = "Guardado";
            $scope.email.id = email.id
            $uibModalInstance.close($scope.email);
          },
          function(error){ $uibModalInstance.dismiss(error); }
        )
      }

      //Inicializar
      init();

    }
})();

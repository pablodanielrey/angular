 (function() {
    'use strict';

    angular
        .module('offices.admin')
        .controller('AddUserModalCtrl', AddUserModalCtrl);

    AddUserModalCtrl.$inject = ['$scope', '$uibModalInstance', 'OfficesAdmin', 'officeId'];

    function AddUserModalCtrl($scope, $uibModalInstance, OfficesAdmin, officeId) {

      $scope.component = { disabled: false, message: null };

      //Inicializar componente
      var init = function(){
        $scope.officeId = officeId;

        $scope.user = null; //usuario seleccionado
        $scope.user_ = {search:null, selected:null}  //Objeto para ser utilizado en la vista, en el formulario de typeahead
      };


      //Enviar formulario
      $scope.submit = function(){
        $scope.component.disabled = true;
        $scope.component.message = "Procesando";

        if(!$scope.user){
          $scope.component.message = "Seleccione usuario";
          return;
        }

        OfficesAdmin.getUsers($scope.officeId).then(
          function(users) {
            if (include($scope.user, users)) {
              $uibModalInstance.close(null);
              return;
            }
            $scope.addUser();

          })

      }

      function include(user, users) {
        if (user == null || users.length < 1) return true;
        for (var i = 0; i < users.length; i++) {
          if (user.id == users[i].id) {
            return true;
          }
        }
      }

      $scope.addUser = function() {
        OfficesAdmin.addUser($scope.officeId, $scope.user.id).then(
          function(response){
            $scope.component.message = "Guardado";
            $uibModalInstance.close($scope.user);
          },
          function(error){ $uibModalInstance.dismiss(error); }
        )
      }


      //Buscar usuarios para seleccionar
      $scope.searchUsers = function(search) {
        $scope.user_.search = search; //cache de busqueda
        if (search.length < 3) return "";

        return OfficesAdmin.searchUsers(search).then(
          function(users){ return users; },
          function(error){
            alert("Error");
            console.log(error);
          }
        )
      };


      $scope.selectUser = function(){
        if(($scope.user_.selected) && (typeof $scope.user_.selected === "object")){
          $scope.user = $scope.user_.selected;
          return true;
        }

        $scope.user = null;
        return false;
      };

      $scope.cancel = function() {
        $scope.user = null;
        $uibModalInstance.close(null);
      }


      //Inicializar
      init();

    }
})();

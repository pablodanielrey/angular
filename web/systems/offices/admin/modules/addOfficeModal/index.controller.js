 (function() {
    'use strict';

    angular
        .module('offices.admin')
        .controller('AddOfficeModalCtrl', AddOfficeModalCtrl);

    AddOfficeModalCtrl.$inject = ['$scope', '$uibModalInstance', 'OfficesAdmin', 'userId'];

    function AddOfficeModalCtrl($scope, $uibModalInstance, OfficesAdmin, userId) {

      $scope.component = { disabled: false, message: null };

      //Inicializar componente
      var init = function(){
        $scope.userId = userId;

        $scope.office = {search:null, selected:null}  //Objeto para ser utilizado en la vista, en el formulario de typeahead
      };


      //Enviar formulario
      $scope.submit = function(){
        $scope.component.disabled = true;
        $scope.component.message = "Procesando";

        if(!$scope.office.selected){
          $scope.component.message = "Seleccione oficina";
          return;
        }

        OfficesAdmin.addUser($scope.office.selected.id, $scope.userId).then(
          function(response){
            $scope.component.message = "Guardado";
            $uibModalInstance.close($scope.office.selected);
          },
          function(error){ $uibModalInstance.dismiss(error); }
        )


      }


      //Buscar oficinas para seleccionar
      $scope.searchOffices = function(search) {
        $scope.office.search = search; //cache de busqueda
        if (search.length < 3) return "";

        return OfficesAdmin.searchOffices(search).then(
          function(offices){ return offices; },
          function(error){ console.log(error); }
        )
      };


      $scope.selectOffice = function(){
        if(($scope.office.selected) && (typeof $scope.office.selected === "object")){
          return true;
        }

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

 (function() {
    'use strict';

    angular
        .module('offices.admin')
        .controller('AdminOfficeCtrl', AdminOfficeCtrl);

    AdminOfficeCtrl.$inject = ['$scope', '$timeout', '$q', '$location', 'OfficesAdmin'];


    function AdminOfficeCtrl($scope, $timeout, $q, $location, OfficesAdmin) {

      $scope.component = {
        disabled: true, //flag para indicar si el formulario esta deshabilitado o no
        message: "Inicializando", //mensaje
      };


      //Inicializar componente
      var init = function(){
        var urlParams = $location.search();
        if("id" in urlParams) {
          $scope.officeId = urlParams["id"];
          $scope.action = 'edit';
        } else {
          $scope.action = 'create';
        }

         OfficesAdmin.admin($scope.officeId).then(
          function(office){
            $scope.office = office;
            $scope.component.disabled = false;
            $scope.component.message = null;
            $scope.$apply()
          },
          function(error){
             alert("error");
             console.log(error);
          }
        )
      };

      $scope.back = function() {
        window.history.back();
      }

      //Enviar formulario
      $scope.submit = function(){
        $scope.component.disabled = true;
        $scope.component.message = "Procesando";

        OfficesAdmin.persist($scope.office).then(
          function(response){
            $scope.component.message = "Guardado";
            $scope.$apply();
          },
          function(error){
             alert("error")
             console.log(error)
          }
        )

      }


      //Inicializar
      $timeout(init, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

    }
})();

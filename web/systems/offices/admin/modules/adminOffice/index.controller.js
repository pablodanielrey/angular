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
        id: null //Identificacion de la entidad que esta siendo administrada
      };

      var urlParams = $location.search();
      if("id" in urlParams) $scope.component.id = urlParams["id"];

      $scope.office = null
      $scope.designations = [];

      //Inicializar componente
      var init = function(){
        var pr0 = OfficesAdmin.admin($scope.component.id)
        var pr1 = ($scope.component.id) ? OfficesAdmin.getDesignations($scope.component.id) : $q.when([])

        $q.all([pr0, pr1]).then(
          function(responses){
            $scope.office = responses[0];
            $scope.designations = responses[1];

            $scope.component.disabled = false;
            $scope.component.message = null;
          },
          function(error){
             alert("error")
             console.log(error)
          }
        )
      };



      //Enviar formulario
      $scope.submit = function(){
        $scope.component.disabled = true;
        $scope.component.message = "Procesando";
        /*
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
        */
      }

      //Agregar / eliminar telefono
      $scope.addDesignation = function() {
        $scope.designations.push({__json_class__:"OfficeDesignation", __json_module__
  :"model.offices.entities.OfficeDesignation", user:null, userId:null, officeId:$scope.component.id})
      };
      $scope.deleteDesignation = function(index){ $scope.designations.splice(index, 1); }; //Eliminar telefono



      //Buscar usuarios para seleccionar
      $scope.searchUsers = function(search, $index) {
        $scope.designations[$index]["_search"] = search; //cache de busqueda
        if (search.length < 4) return "";

        return OfficesAdmin.searchUsers(search).then(
          function(users){ return users; },
          function(error){
            alert("Error");
            console.log(error);
          }
        )
      };


      $scope.selectUser = function($index){
        if(($scope.designations[$index]["_selected"]) && (typeof $scope.designations[$index]["_selected"] === "object")){
          $scope.designations[$index]["user"] = $scope.designations[$index]["_selected"];
          $scope.designations[$index]["userId"] = $scope.designations[$index]["_selected"]["id"];
          return $index;
        }

        else if(($scope.designations[$index]["userId"]) && (!$scope.designations[$index]["_search"])){
          return $index;
        }

        $scope.designations[$index]["userId"] = null;
        return false;
      };





      //Inicializar
      $timeout(init, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

    }
})();

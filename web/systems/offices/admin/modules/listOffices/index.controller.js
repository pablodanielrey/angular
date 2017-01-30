 (function() {
    'use strict';

    angular
        .module('offices.admin')
        .controller('ListOfficesCtrl', ListOfficesCtrl);

    ListOfficesCtrl.$inject = ['$scope', '$timeout', 'OfficesAdmin'];


    function ListOfficesCtrl($scope, $timeout, OfficesAdmin) {

      $scope.component = { disabled:true, message:"Inicializando" };

      var init = function(){
        OfficesAdmin.getOffices().then(
          function(offices){
            $scope.offices = offices;
            $scope.component.disabled = false;
            $scope.component.message = null;
            $scope.$apply();
          }
        )
      }

      $timeout(init, 500); //TODO reemplazar por evento de inicializacion de Login

    }
})();

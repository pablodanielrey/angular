 (function() {
    'use strict';

    angular
        .module('offices.admin')
        .controller('ListOfficesCtrl', ListOfficesCtrl);

    ListOfficesCtrl.$inject = ['$scope', '$timeout', 'OfficesAdmin'];


    function ListOfficesCtrl($scope, $timeout, OfficesAdmin) {

      $scope.offices = []; //lista de oficinas

      var init = function(){
        OfficesAdmin.getOffices().then(
          function(offices){
            console.log(offices)
            $scope.offices = offices;
            $scope.$apply();
          }
        )
      }


      $timeout(init, 500); //TODO reemplazar por evento de inicializacion de Login

    }
})();

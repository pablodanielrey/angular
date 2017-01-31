 (function() {
    'use strict';

    angular
        .module('offices.admin')
        .controller('ListOfficesByUserCtrl', ListOfficesByUserCtrl);

    ListOfficesByUserCtrl.$inject = ['$scope', '$timeout', '$location', 'OfficesAdmin'];


    function ListOfficesByUserCtrl($scope, $timeout, $location, OfficesAdmin) {

      $scope.component = { disabled:true, message:"Inicializando" };

      var init = function(){
        var urlParams = $location.search();
        if("userId" in urlParams) $scope.userId = urlParams["userId"];

        OfficesAdmin.getOfficesByUser($scope.userId).then(
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

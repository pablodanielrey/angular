 (function() {
    'use strict';

    angular
        .module('offices.admin')
        .controller('ListOfficesCtrl', ListOfficesCtrl);

    ListOfficesCtrl.$inject = ['$scope', '$timeout', '$routeParams', '$location', 'OfficesAdmin'];


    function ListOfficesCtrl($scope, $timeout, $routeParams, $location, OfficesAdmin) {

      $scope.search = { disabled:true, message:"Inicializando", text: '' };

      var init = function(){
        OfficesAdmin.getOffices().then(
          function(offices){
            $scope.offices = offices;
            $scope.search.disabled = false;
            $scope.search.message = null;
            $scope.$apply();

            var params = $routeParams;
            if ('search' in params) {
              $timeout(function() { $scope.search.text = params.search;}, 0)
            }
          }
        )
      }

      $scope.edit  = function(office) {

        $location.path("/adminOffice/").search({id:office.id, search: $scope.search.text});
      }
      $timeout(init, 500); //TODO reemplazar por evento de inicializacion de Login

    }
})();

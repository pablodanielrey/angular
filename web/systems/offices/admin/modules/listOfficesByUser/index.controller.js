 (function() {
    'use strict';

    angular
        .module('offices.admin')
        .controller('ListOfficesByUserCtrl', ListOfficesByUserCtrl);

    ListOfficesByUserCtrl.$inject = ['$scope', '$timeout', '$location', '$uibModal', 'OfficesAdmin'];


    function ListOfficesByUserCtrl($scope, $timeout, $location, $uibModal, OfficesAdmin) {

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

      //Open modal add email
      $scope.addOffice = function () {
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: "modules/addOfficeModal/index.html?t=" + new Date().getTime(),
          controller: "AddOfficeModalCtrl",
          resolve: {
            userId: function () { return $scope.userId; }
          }
        });

        modalInstance.result.then(
           function (office) { if (office != null) $scope.offices.push(office); },
           function (error) { console.log(error); }
         );
       };

      $scope.deleteOffice = function($index){
        console.log($index);
        OfficesAdmin.deleteUser($scope.offices[$index].id, $scope.userId).then(
          function(response){
             $scope.offices.splice($index, 1);
             $scope.$apply();
          },
          function(error){ console.log(error) }
        );
      }

      $timeout(init, 500); //TODO reemplazar por evento de inicializacion de Login

    }

})();

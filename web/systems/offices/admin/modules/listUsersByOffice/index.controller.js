 (function() {
    'use strict';

    angular
        .module('offices.admin')
        .controller('ListUsersByOfficeCtrl', ListUsersByOfficeCtrl);

    ListUsersByOfficeCtrl.$inject = ['$scope', '$timeout', '$location', '$uibModal', 'OfficesAdmin', 'Login'];


    function ListUsersByOfficeCtrl($scope, $timeout, $location, $uibModal, OfficesAdmin, Login) {

      $scope.component = { disabled: true, message: "Inicializando" };

      function init(){
        var urlParams = $location.search();
        if("id" in urlParams) {
          $scope.officeId = urlParams["id"];
          $scope.action = 'edit';
        } else {
          $scope.action = 'create';
        }

        OfficesAdmin.getUsers($scope.officeId).then(
          function(users){
            $scope.component.disabled = false;
            $scope.component.message = null;
            $scope.users = users;
            $scope.$apply();
          },
          function(error){
             alert("error");
             console.log(error);
          }
        )
      }

      $scope.back = function() {
        window.history.back();
      }

      //Open modal add email
      $scope.addUser = function () {
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: "modules/addUserModal/index.html?t=" + new Date().getTime(),
          controller: "AddUserModalCtrl",
          resolve: {
            officeId: function () { return $scope.officeId; }
          }
        });

        modalInstance.result.then(
           function (user) { if (user != null) $scope.users.push(user); },
           function (error) { console.log(error); }
         );
       };


       $scope.deleteUser = function(index){
         OfficesAdmin.deleteUser($scope.officeId, $scope.users[index].id).then(
           function(response){
             $scope.users.splice(index, 1);
             $scope.$apply();
           },
           function(error){
              alert("error")
              console.log(error);
           }
         )
       }

      $timeout(init, 500); //TODO reemplazar $timeout por algun evento que indique inicializacion

    }
})();

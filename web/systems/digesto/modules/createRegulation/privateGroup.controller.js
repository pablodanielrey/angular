angular
    .module('mainApp')
    .controller('PrivateGroupCtrl',PrivateGroupCtrl)

PrivateGroupCtrl.$inject = ['$rootScope','$scope']

function PrivateGroupCtrl($rootScope,$scope) {


  $scope.initialize = initialize;
  $scope.addOffice = addOffice;
  $scope.removeOffice = removeOffice;


  /* -------------------------------------------------------------
   * ----------------------------- EVENTOS -----------------------
   * -------------------------------------------------------------
   */

  $scope.$on('openPrivateGroupEvent',function(event) {
    $scope.initialize();
  });


  /* -------------------------------------------------------------
   * -------------------------- INICIALIZACION -------------------
   * -------------------------------------------------------------
   */

  function initialize() {
    console.log($scope.model.offices);
    $scope.$emit('viewPrivateGroupLoad');
  }


  /* -------------------------------------------------------------
   * ----------------------------- ACCIONES ----------------------
   * -------------------------------------------------------------
   */

   function addOffice() {

   }

   function removeOffice() {

   }
}

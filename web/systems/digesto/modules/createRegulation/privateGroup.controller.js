angular
    .module('mainApp')
    .controller('PrivateGroupCtrl',PrivateGroupCtrl)

PrivateGroupCtrl.$inject = ['$rootScope','$scope']

function PrivateGroupCtrl($rootScope,$scope) {

  $scope.model.filteredOffices = []

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
    $scope.model.search.allOffice = '';
    console.log($scope.model.offices);
    loadFilteredOffices();
    $scope.$emit('viewPrivateGroupLoad');
  }


  /* -------------------------------------------------------------
   * ---------------------- FILTRO DE OFICINAS -------------------
   * -------------------------------------------------------------
   */

  function loadFilteredOffices() {
    $scope.model.filteredOffices = [];
    for (var i = 0; i < $scope.model.offices.length; i++) {
      var o1 = $scope.model.offices[i];
      var include = false;

      for (var j = 0; j < $scope.model.normative.offices.length; j++) {
        var o2 = $scope.model.normative.offices[j];
        if (o1.id == o2.id) {
          include = true;
          break;
        }
      }

      if (!include) {
        $scope.model.filteredOffices.push(o1);
      }
    }
  }


  /* -------------------------------------------------------------
   * ----------------------------- ACCIONES ----------------------
   * -------------------------------------------------------------
   */

   function addOffice(office) {
     $scope.model.normative.offices.push(office);
     loadFilteredOffices();
   }

   function removeOffice(office) {
     var index = $scope.model.normative.offices.indexOf(office);
     $scope.model.normative.offices.splice(index,1);
     loadFilteredOffices();
   }
}

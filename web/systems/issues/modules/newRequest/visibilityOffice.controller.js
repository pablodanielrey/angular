angular
    .module('mainApp')
    .controller('VisibilityOfficesCtrl',VisibilityOfficesCtrl);

VisibilityOfficesCtrl.$inject =  ['$rootScope', '$scope', 'Notifications', 'Office']

function VisibilityOfficesCtrl($rootScope,$scope,Notifications,Office) {


  // ----------------------------------------------------------
  // -------------- DEFINICION DE METODOS ---------------------
  // ----------------------------------------------------------
  $scope.initialize = initialize;


  // -------------------------------------------------------------
  // ------------------------- EVENTOS ---------------------------
  // -------------------------------------------------------------
  $scope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });


  // ----------------------------------------------------------
  // ----------------- INICIALIZACION -------------------------
  // ----------------------------------------------------------
  function initialize() {

  }

}

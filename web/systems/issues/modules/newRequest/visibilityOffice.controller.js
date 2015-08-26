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
  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });


  // ----------------------------------------------------------
  // ----------------- INICIALIZACION -------------------------
  // ----------------------------------------------------------
  function initialize() {
    loadOffices();
  }

  function loadOffices() {
    Office.getOfficesTreeByUser(null,
      function(offices) {
        if (offices.length == 0) {
          $scope.model.offices = [];
          return;
        }
        $scope.model.offices = offices;
        var o = $scope.model.offices[0];
        o['childrens'] = [{name:'Programacion',childrens:[{name:'Diseño',childrens:[]}]}];
        $scope.model.offices.push({name:'Detise',childrens:[]});
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }

}

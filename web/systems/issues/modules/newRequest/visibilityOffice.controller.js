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
        for (var i = 0; i < offices.length; i++) {
          o = offices[i];
          o['tree'] = false;
        }
        $scope.model.offices = offices;
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }

  // ----------------------------------------------------------
  // --------------------- ACCIONES ---------------------------
  // ----------------------------------------------------------
  $scope.selectTree = selectTree;
  $scope.selectOffice = selectOffice;

  function selectTree(office) {
    if (!office.selected) {
      office.selected = !office.selected;
    }
    changeChildrens(office,office.tree);
  }

  function selectOffice(office) {
    if (office.tree) {
      office.tree = office.selected;
      if (!office.tree) {
        changeChildrens(office,false);
      }
    }
  }

  function changeChildrens(office,value) {
    if (office.childrens) {
      for (var i = 0; i < office.childrens.length; i++) {
          office.childrens[i].selected = value;
          office.childrens[i].disabled = value;
          changeChildrens(office.childrens[i],value);
      }
    }
  }


}

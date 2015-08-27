angular
    .module('mainApp')
    .controller('VisibilityOfficesCtrl',VisibilityOfficesCtrl);

VisibilityOfficesCtrl.$inject =  ['$rootScope', '$scope', 'Notifications', 'Office']

function VisibilityOfficesCtrl($rootScope,$scope,Notifications,Office) {

  $scope.model.issueSelected = {}


  // visibility = {'office_id':'','tree':false}

  // ----------------------------------------------------------
  // -------------- DEFINICION DE METODOS ---------------------
  // ----------------------------------------------------------
  $scope.initialize = initialize;


  // -------------------------------------------------------------
  // ------------------------- EVENTOS ---------------------------
  // -------------------------------------------------------------
  $rootScope.$on('$viewContentLoaded', function(event) {
    loadOffices();
    $scope.initialize(null);
  });

  $scope.$on('displayVisbilityEvent',function(event,issue) {
    $scope.initialize(issue);
    initializeOffices($scope.model.offices);
    for (var i = 0; i < issue.visibilities.length; i++) {
      var v = issue.visibilities[i];
      changeVisibilities($scope.model.offices,v);
    }
  });

  function changeVisibilities(offices,v) {
    for (var i = 0; i < offices.length; i++) {
      var o = offices[i];
      if (o.id == v.office_id) {
        o.selected = true;
        if (v.tree) {
          o.tree = true;
          changeChildrens(o,true);
        }
        return;
      }
      changeVisibilities(o.childrens,v);
    }
  }


  // ----------------------------------------------------------
  // ----------------- INICIALIZACION -------------------------
  // ----------------------------------------------------------
  function initialize(issue) {
    $scope.model.issueSelected = issue;
  }

  function initializeOffices(offices) {
    for (var i = 0; i < offices.length; i++) {
      o = offices[i];
      o['tree'] = false;
      o['selected'] = false;
      o['disabled'] = false;
      initializeOffices(o.childrens);
    }
  }

  function loadOffices() {
    Office.getOfficesTreeByUser(null,
      function(offices) {
        if (offices.length == 0) {
          $scope.model.offices = [];
          return;
        }
        initializeOffices(offices);
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
  $scope.saveVisibility = saveVisibility;
  $scope.cancelVisibility = cancelVisibility;

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

  function getSelecteds(offices) {
    selecteds = [];
    for (var i = 0; i < offices.length; i++) {
      var off = offices[i];
      if (off.tree) {
        selecteds.push({'office_id':off.id,'tree':off.tree,'type':'OFFICE'});
        continue;
      }
      if (off.selected) {
        selecteds.push({'office_id':off.id,'tree':off.tree,'type':'OFFICE'});
      }
      selecteds = selecteds.concat(getSelecteds(off.childrens));
    }
    return selecteds;
  }

  function saveVisibility() {
    selecteds = getSelecteds($scope.model.offices);
    $scope.$emit('saveVisibilityEvent',$scope.model.issueSelected,selecteds);
  }

  function cancelVisibility() {
    $scope.$emit('cancelVisibilityEvent');
  }
}

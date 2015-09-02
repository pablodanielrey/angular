angular
    .module('mainApp')
    .controller('AssignedCtrl',AssignedCtrl);

AssignedCtrl.$inject =  ['$rootScope', '$scope', 'Notifications', 'Office']

function AssignedCtrl($rootScope,$scope,Notifications,Office) {

  $scope.model.issueSelected = {}


  // ----------------------------------------------------------
  // -------------- DEFINICION DE METODOS ---------------------
  // ----------------------------------------------------------
  $scope.initialize = initialize;

  $scope.saveAssigned = saveAssigned;
  $scope.cancelAssigned = cancelAssigned;
  $scope.isReadOnly = isReadOnly;

  $scope.selectOffice = selectOffice;


  // -------------------------------------------------------------
  // ------------------------- EVENTOS ---------------------------
  // -------------------------------------------------------------
  $rootScope.$on('$viewContentLoaded', function(event) {
    loadOffices();
    $scope.initialize(null);
  });

  $scope.$on('displayAssignedEvent',function(event,issue) {
    $scope.initialize(issue);
    initializeOffices($scope.model.offices);
    var offices = [];
    for (var i =0; i < $scope.model.offices.length; i++) {
      offices.push($scope.model.offices[i]);
    }
    while (offices.length > 0) {
      var o = offices[0];
      offices.splice(0,1);
      if (issue['office_id'] == o['id']) {
        o.selected = true;
        $scope.model.officeSelected = o;
        break;
      }
      offices = offices.concat(o['childrens']);
    }
  });


  // ----------------------------------------------------------
  // ----------------- INICIALIZACION -------------------------
  // ----------------------------------------------------------
  function initialize(issue) {
    $scope.model.issueSelected = issue;
    if (issue != null) {
      var v = (issue['readOnly']) ? issue['readOnly']:false;
      $scope.model.issueSelected.readOnly = v;
    }
  }

  function initializeOffices(offices) {
    $scope.model.otherOffices = [];
    for (var i = 0; i < offices.length; i++) {
      o = offices[i];
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

  function isReadOnly() {
    return $scope.model.issueSelected != null && $scope.model.issueSelected.readOnly
  }

  function selectOffice(office) {
    $scope.model.officeSelected = office;
  }


  function saveAssigned() {
    o = $scope.model.officeSelected;
    selecteds = [];
    selecteds.push(o);
    $scope.$emit('saveAssignedEvent',$scope.model.issueSelected,selecteds);
  }

  function cancelAssigned() {
    $scope.$emit('cancelAssignedEvent');
  }
}

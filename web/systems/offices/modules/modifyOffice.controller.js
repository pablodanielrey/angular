angular
    .module('mainApp')
    .controller('ModifyOfficeController',ModifyOfficeController);

ModifyOfficeController.$inject = ['$scope', 'Session', 'Notifications', 'Office'];

function ModifyOfficeController($scope, Session, Notifications, Office) {

  var vm = this;
  vm.model = {
    sessionUserId: {},
    offices: [],
    searchOffice: '',
    selectedOffice: null,
    action: '',
    office: null
  }

  vm.initialize = initialize;
  vm.loadOffices = loadOffices;
  vm.selectOffice = selectOffice;
  vm.create = create;
  vm.modify = modify;

  function initialize() {
    var session = Session.getCurrentSession();
    vm.model.sessionUserId = session.user_id;

    vm.loadOffices();
    vm.model.searchOffice = '';
    vm.model.selectedOffice = null;

    vm.model.action = null;
    vm.model.office = null;
  }

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.$parent.itemSelected('modifyOffice');
    vm.initialize();
  });


  // -------------------------------------
  // -------- Listado de oficinas --------
  // -------------------------------------

  function loadOffices() {
    vm.model.offices = [];
    var userId = vm.model.sessionUserId;
    var tree = true;
    var role = 'autoriza';

    Office.getOfficesByUserRole(userId,role,tree,
      function(offices) {
        if (offices != null) {
          vm.model.offices = offices;
        }
      },
      function(error) {
          Notification.message(error);
      }
    );
  }

  function setParentOffice(office, offices) {
    for (var i = 0; i < offices.length; i++) {
      if (office.parent == offices[i].id) {
        office.parentObj = offices[i];
        office.order = 1;
        return ;
      }
    }
    office.parentObj = office;
    office.order = 0;
  }

  function selectOffice(office) {
    if (vm.model.selectedOffice == office) {
      vm.model.selectedOffice = null;
      vm.model.action = null;
    } else {
      vm.model.selectedOffice = office;
    }
  }


  // ----------------------------------------------
  // ---------------- ACTIONS ---------------------
  // ----------------------------------------------

  function create() {
    vm.model.action = 'create';
    vm.model.office = {};
    vm.model.selectedOffice = null;
  }

  function modify() {
    vm.model.action = 'modify';
    vm.model.officesModify = angular.copy(vm.model.offices);
    for (var i = 0; i < vm.model.officesModify.length; i ++) {
      setParentOffice(vm.model.officesModify[i], vm.model.officesModify);
      if (vm.model.selectedOffice.id == vm.model.officesModify[i].id) {
        vm.model.office = vm.model.officesModify[i];
      }
    }

    if (vm.model.office.id == vm.model.office.parentObj.id ) {
      vm.model.office.parentObj = null;
    }

    var index = vm.model.officesModify.indexOf(vm.model.office);
    if (index > -1) {
      vm.model.officesModify.splice(index, 1);
    }

  }

}

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
    action: null,
    office: null
  }

  vm.initialize = initialize;
  vm.loadOffices = loadOffices;
  vm.selectOffice = selectOffice;
  vm.create = create;
  vm.modify = modify;
  vm.cancel = cancel;
  vm.save = save;

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
        office.parentName = offices[i].name;
        office.order = 1;
        return ;
      }
    }
    office.parentName = office.name;
    office.order = 0;
  }

  function selectOffice(office) {
    console.log(office);
    if (vm.model.selectedOffice == office) {
      vm.model.selectedOffice = null;
      vm.model.action = null;
    } else {
      vm.model.selectedOffice = office;
      vm.modify();
    }
  }


  // ----------------------------------------------
  // ---------------- ACTIONS ---------------------
  // ----------------------------------------------

  function copyOffices() {
    vm.model.officesModify = angular.copy(vm.model.offices);
    for (var i = 0; i < vm.model.officesModify.length; i ++) {
      setParentOffice(vm.model.officesModify[i], vm.model.officesModify);
      if (vm.model.selectedOffice != null && vm.model.selectedOffice.id == vm.model.officesModify[i].id) {
        vm.model.office = vm.model.officesModify[i];
      }
    }
  }

  function create() {
    vm.model.action = 'create';
    vm.model.office = {};
    vm.model.selectedOffice = null;
    copyOffices();
  }

  function modify() {
    vm.model.action = 'modify';
    copyOffices();

    if (vm.model.office.id == vm.model.office.parentObj.id ) {
      vm.model.office.parentObj = null;
    }

    var index = vm.model.officesModify.indexOf(vm.model.office);
    if (index > -1) {
      vm.model.officesModify.splice(index, 1);
    }

  }

  function cancel() {
    vm.model.action = null;
    vm.model.selectedOffice = null;
  }

  function save() {
    // verificacion de los campos
    if (vm.model.office.name == null || vm.model.office.name.trim() == '') {
      return;
    }

    if (vm.model.office.parentObj != null) {
      vm.model.office.parent = vm.model.office.parentObj.id;
    } else {
      vm.model.office.parent = null;
    }

    Office.persistOffice(vm.model.office,
      function(ok) {
        vm.loadOffices();
        vm.model.action = null;
        vm.model.selectedOffice = null;
        Notifications.message('Se ha guardado exitósamente');
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }

}

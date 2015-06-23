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
    selectedOffice: null
  }

  vm.initialize = initialize;
  vm.loadOffices = loadOffices;
  vm.selectOffice = selectOffice;

  function initialize() {
    var session = Session.getCurrentSession();
    vm.model.sessionUserId = session.user_id;

    vm.loadOffices();
    vm.model.searchOffice = '';
    vm.model.selectedOffice = null;
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
          for (var i = 0; i < offices.length; i++) {
            setParentOffice(offices[i], offices);
          }
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
        office.parentName = offices[i].name;
        office.order = 1;
        return ;
      }
    }
    office.parentName = office.name;
    office.order = 0;
  }

  function selectOffice(office) {
    if (vm.model.selectedOffice == office) {
      vm.model.selectedOffice = null;
    } else {
      vm.model.selectedOffice = office;
    }
  }

}

angular
    .module('mainApp')
    .controller('RolesOfficesController',RolesOfficesController);

RolesOfficesController.$inject = ['$scope','$location','Notifications', 'Session', 'Office'];

function RolesOfficesController($scope, $lcoation, Notifcations, Session, Office) {

  var vm = this;
  vm.model = {
    sessionUserId: '',
    searchOffice: '',
    offices: [],
    selectedOffices: []
  }

  vm.initialize = initialize;
  vm.initializeOffices = initializeOffices;
  vm.isSelectedOffice = isSelectedOffice;
  vm.selectOffice = selectOffice;
  vm.loadOffices = loadOffices;


  function initialize() {
    var session = Session.getCurrentSession();
    vm.model.sessionUserId = session.user_id;

    vm.initializeOffices();
  }

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.$parent.itemSelected('rolesOffices');
    vm.initialize();
  });


  // -----------------------------------------------
  // ---------------- OFICINAS ---------------------
  // -----------------------------------------------

  function initializeOffices() {
    vm.model.searchOffice = '';
    vm.model.offices = [];
    vm.model.selectedOffices = [];
    vm.loadOffices();
  }

  function isSelectedOffice(office) {
    return include(vm.model.selectedOffices,office);
  }

  function selectOffice(office) {
    if (vm.isSelectedOffice(office)) {
      // la deselecciono
      removeItem(vm.model.selectedOffices,office);
    } else {
      // la selecciono
      vm.model.selectedOffices.push(office);
    }
  }

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

  // ----------------------------------
  // -------------- UTILS -------------
  // ----------------------------------

  function removeItem(array,item) {
    var  index = array.indexOf(item);
    if (index > -1) {
      array.splice(index,1);
    }
  }

  function include(array,item) {
    var  index = array.indexOf(item);
    return index > -1;
  }

}

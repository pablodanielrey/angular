angular
    .module('mainApp')
    .controller('RolesOfficesController',RolesOfficesController);

RolesOfficesController.$inject = ['$scope','$location','Notifications', 'Session', 'Office', 'Users'];

function RolesOfficesController($scope, $lcoation, Notifcations, Session, Office, Users) {

  var vm = this;
  vm.model = {
    sessionUserId: '',
    searchOffice: '',
    offices: [],
    selectedOffices: [],
    searchUser: '',
    users: [],
    selectedUsers: [],
    roles: [],
    selectedRoles: []
  };

  vm.view = {
    displayContentRole: false
  };

  vm.initialize = initialize;

  vm.initializeOffices = initializeOffices;
  vm.isSelectedOffice = isSelectedOffice;
  vm.selectOffice = selectOffice;
  vm.loadOffices = loadOffices;

  vm.initializeUsers = initializeUsers;
  vm.isSelectedUser = isSelectedUser;
  vm.selectUser = selectUser;
  vm.loadUsers = loadUsers;
  vm.loadUserData = loadUserData;

  vm.initializeRole = initializeRole;
  vm.isDisplayContentRole = isDisplayContentRole;
  vm.isSelectedRole = isSelectedRole;
  vm.selectRole = selectRole;
  vm.loadRoles = loadRoles;

  function initialize() {
    var session = Session.getCurrentSession();
    vm.model.sessionUserId = session.user_id;

    vm.initializeOffices();
    vm.initializeUsers();

    vm.initializeRole();
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
      if (!vm.isSelectedOffice(office.parentObj)) {
        // la deselecciono
        removeItem(vm.model.selectedOffices,office);
        for (var i = 0; i < office.childrens.length; i++) {
          removeItem(vm.model.selectedOffices,office.childrens[i]);
        }
      }
    } else {
      // la selecciono
      vm.model.selectedOffices.push(office);
      for (var i = 0; i < office.childrens.length; i++) {
        var child = office.childrens[i];
        if (!vm.isSelectedOffice(child)) {
          vm.model.selectedOffices.push(child);
        }
      }
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
          //  seteo los hijos
          for (var i = 0; i < offices.length; i ++) {
            offices[i].childrens = [];
            setChildrens(offices,offices[i]);
          }

          // agrego solo los que no tienen padre
          for (var i = 0; i < offices.length; i ++) {
            if (offices[i].parentObj === undefined) {
              vm.model.offices.push(offices[i]);
            }
          }
        }
      },
      function(error) {
          Notification.message(error);
      }
    );
  }

  function setChildrens(offices, office) {
    for (var i = 0; i < offices.length; i ++) {
      if (offices[i].parent == office.id) {
        office.childrens.push(offices[i]);
        offices[i].parentObj = office;
      }
    }
  }

  // ----------------------------------
  // ----------- USUARIOS -------------
  // ----------------------------------

  function initializeUsers() {
    vm.model.searchUser = '';
    vm.model.users = [];
    vm.model.selectedUsers = [];
    vm.loadUsers();
  }

  function isSelectedUser(user) {
    return include(vm.model.selectedUsers,user);
  }

  function selectUser(user) {
    if (vm.isSelectedUser(user)) {
      // la deselecciono
      removeItem(vm.model.selectedUsers,user);
    } else {
      // la selecciono
      vm.model.selectedUsers.push(user);
    }
  }

  function loadUserData(userId) {
    Users.findUser(userId,
      function(user) {
        vm.model.users.push(user);
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }

  function loadUsers() {
    vm.model.users = [];
    var userId = vm.model.sessionUserId;
    var tree = true;
    var role = 'autoriza';

    Office.getUserInOfficesByRole(userId, role, tree,
      function(users) {
        for (var i = 0; i < users.length; i++) {
          vm.loadUserData(users[i]);
        }
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }

  // -----------------------------------------------
  // ----------------- ROLES -----------------------
  // -----------------------------------------------

  function initializeRole() {
    vm.view.displayContentRole = false;
    vm.loadRoles();
  }

  function clearRole() {
    vm.model.roles = [];
    vm.model.selectedRoles = [];
  }

  $scope.$watch('vm.model.selectedUsers.length',function(newValue, oldValue) {
    if (newValue > 0 && vm.model.selectedOffices.length > 0) {
      vm.view.displayContentRole = true;
      clearRole();
    } else {
      vm.view.displayContentRole = false;
    }
  });

  $scope.$watch('vm.model.selectedOffices.length',function(newValue, oldValue) {
    if (newValue > 0 && vm.model.selectedUsers.length > 0) {
      vm.view.displayContentRole = true;
      clearRole();
    } else {
      vm.view.displayContentRole = false;
    }
  });

  function isDisplayContentRole() {
    return vm.view.displayContentRole;
  }

  function isSelectedRole(role) {
    return include(vm.model.selecteRoles,role);
  }

  function selectRole(role) {
    if (vm.isSelectedRole(role)) {
      // la deselecciono
      removeItem(vm.model.selectedRoles,role);
    } else {
      // la selecciono
      vm.model.selectedRoles.push(role);
    }
  }

  function loadRoles() {
    clearRole();
    Office.
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

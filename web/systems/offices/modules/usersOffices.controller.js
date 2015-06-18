angular
    .module('mainApp')
    .controller('UsersOfficesController',UsersOfficesController);

UsersOfficesController.$inject = ['$scope','$location','Notifications', 'Office', 'Users'];

function UsersOfficesController($scope, $location, Notifications, Office, Users) {

  var vm = this;

  vm.model = {
    officeSelected: null,
    allOffices: [],
    users: [],
    usersOffice: [],
    officeChange: null
  }

  vm.initialize = initialize;
  vm.initalizeAllUsers = initializeAllUsers;
  vm.initializeUsersOffice = initializeUsersOffice;
  vm.loadOffices = loadOffices;
  vm.addUser = addUser;
  vm.removeUser = removeUser;

  function initialize() {
    vm.initalizeAllUsers();
    vm.initializeUsersOffice();
  }

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.$parent.itemSelected('usersOffices');
    vm.initialize();
  });


  // //////////////////////////////////////////////////////
  // /////////////////////// FILTROS //////////////////////
  // //////////////////////////////////////////////////////
  vm.filterUsers = filterUsers;

  function filterUsers() {
    vm.model.users = [];

    var offices = (vm.model.officeSelected == null) ? vm.model.allOffices : [vm.model.officeSelected];

    var oIds = getOfficesIds(offices);

    Office.getOfficesUsers(oIds,
      function(users) {
        for (var i = 0; i < users.length; i++) {
          loadUserData(users[i]);
        }
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }

  function loadUserData(uid) {
    Users.findUser(uid,
      function(user) {
        vm.model.users.push(user);
        var u = getUser(vm.model.usersOffice,user);
        if (u != null) {
          user.deleted = true;
          removeItem(vm.model.usersOffice, u);
          vm.model.usersOffice.push(user);        
        }
      },
      function(error) {
        Notification.message(error);
      }
    );
  }

  function getUser(users,user) {
    if (users == null || users.length == 0) {
      return null;
    }

    for (var i = 0; i < users.length; i++) {
      if (user.id == users[i].id) {
        return users[i];
      }
    }
  }

  function getOfficesIds(offices) {
    oIds = [];
    for (var i = 0; i < offices.length; i++) {
      oIds.push(offices[i].id);
    }
    return oIds;
  }


  // //////////////////////////////////////////////////////
  // /////////// LISTADO DE USUARIOS A AGREGAR ////////////
  // //////////////////////////////////////////////////////

  function initializeAllUsers() {
    vm.model.users = [];
    vm.loadOffices();
  }

  function loadOffices() {
    vm.model.officeSelected = null;
    vm.model.allOffices = [];
    Office.getOffices(null,
      function(offices) {
        vm.model.allOffices = offices;
        for (var i = 0; i < offices.length; i++) {
          setParentOffice(offices[i], offices);
        }
      },
      function(error) {
        Notifications.message(error);
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


  // //////////////////////////////////////////////////////
  // ///////// LISTADO DE USUARIOS DE LA OFICINA //////////
  // //////////////////////////////////////////////////////

  function initializeUsersOffice() {
    usersOffice = [];
    officeChange = null;
  }


  // //////////////////////////////////////////////////////
  // /////////// AGREGAR-ELIMINAR USUARIO  ////////////////
  // //////////////////////////////////////////////////////

  function addUser(user) {
    user.deleted = true;
    vm.model.usersOffice.push(user);
  }

  function removeUser(user) {
    user.deleted = false;
    removeItem(vm.model.usersOffice, user);
  }


  function removeItem(array,item) {
    var index = array.indexOf(item);
    if (index > -1) {
      array.splice(index, 1);
    }
  }

}

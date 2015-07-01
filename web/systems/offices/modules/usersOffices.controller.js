angular
    .module('mainApp')
    .controller('UsersOfficesController',UsersOfficesController);

UsersOfficesController.$inject = ['$scope','$location','Notifications', 'Office', 'Users', 'Session'];

function UsersOfficesController($scope, $location, Notifications, Office, Users, Session) {

  var vm = this;

  vm.model = {
    officeSelected: null,
    allOffices: [],
    users: [],
    usersOffice: [],
    officesAdmin: [],
    officeChange: null,
    sessionUserId: null
  }

  vm.initialize = initialize;
  vm.initalizeAllUsers = initializeAllUsers;
  vm.initializeUsersOffice = initializeUsersOffice;
  vm.loadOffices = loadOffices;
  vm.loadOfficesAdmin = loadOfficesAdmin;
  vm.addUser = addUser;
  vm.removeUser = removeUser;
  vm.officeChange = officeChange;
  vm.save = save;
  vm.cancel = cancel;

  function initialize() {
    var session = Session.getCurrentSession();
    vm.model.sessionUserId = session.user_id;

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
        updateUsers(user,vm.model.usersOffice);
      },
      function(error) {
        Notification.message(error);
      }
    );
  }

  function updateUsers(user,users) {
    var u = getUser(users,user.id);
    if (u != null) {
      user.deleted = true;
      removeItem(users, u);
      users.push(user);
    }
  }

  function getUser(users,userId) {
    if (users == null || users.length == 0) {
      return null;
    }

    for (var i = 0; i < users.length; i++) {
      if (userId == users[i].id) {
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

    var userId = vm.model.sessionUserId;
    var tree = true;
    var role = 'admin-office';

    Office.getOfficesByUserRole(userId,role,tree,
      function(offices) {
        if (offices != null) {
          vm.model.allOffices = offices;
          for (var i = 0; i < offices.length; i++) {
            setParentOffice(offices[i], offices);
          }
          vm.loadOfficesAdmin();
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


  // //////////////////////////////////////////////////////
  // ///////// LISTADO DE USUARIOS DE LA OFICINA //////////
  // //////////////////////////////////////////////////////

  function initializeUsersOffice() {
    vm.model.usersOffice = [];
    vm.model.officeChange = null;
  }

  function loadOfficesAdmin() {
    vm.model.officesAdmin = angular.copy(vm.model.allOffices);;
  }

  function loadUserDataOffice(uid) {
    Users.findUser(uid,
      function(user) {
        vm.model.usersOffice.push(user);

        // actualizo el listado de usuarios
        if (vm.model.officeSelected == null) {
          return;
        }

        for (var i = 0; i < vm.model.users.length; i++) {
          updateUsers(vm.model.users[i],vm.model.usersOffice);
        }
      },
      function(error) {
          Notifications.message(error);
      }
    );
  }

  function clearUsers(users,usersUpdate) {
    for (var i = 0; i < users.length; i++) {
      users[i].deleted = false;
    }
  }

  function officeChange() {
    clearUsers(vm.model.users);
    vm.model.usersOffice = [];
    if (vm.model.officeChange == null) {
      return;
    }

    var oid = vm.model.officeChange.id;

    Office.getOfficesUsers([oid],
      function(users) {
        vm.model.officeChange.users = users;
        for (var i = 0; i < users.length; i++) {
          loadUserDataOffice(users[i]);
        }
      },
      function(error) {
        Notifications.message(error);
      }
    );

  }


  // //////////////////////////////////////////////////////
  // /////////// AGREGAR-ELIMINAR USUARIO  ////////////////
  // //////////////////////////////////////////////////////

  function addUser(user) {
    if (vm.model.officeChange == null) {
      return;
    }

    var u = getUser(vm.model.usersOffice,user.id);
    if (u == null) {
      vm.model.usersOffice.push(user);
    }

    user.deleted = true;
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


  function save() {
    var newUsers = vm.model.usersOffice.slice();
    var removeUsers = [];

    for (var i = 0; i < vm.model.officeChange.users.length; i++) {
      var userId = vm.model.officeChange.users[i];
      var u = getUser(vm.model.usersOffice, userId);
      if (u == null) {
        removeUsers.push(userId);
      } else {
        removeItem(newUsers,u);
      }
    }

    vm.itemsModify =  newUsers.length + removeUsers.length;

    for (var i = 0; i < newUsers.length; i++) {
      Office.addUserToOffices(newUsers[i].id,vm.model.officeChange.id,
        function(ok) {
          vm.itemsModify = vm.itemsModify -1;
          if (vm.itemsModify == 0) {
            vm.filterUsers();
            vm.officeChange();
            Notifications.message("Se han guardados los cambios exitosamente");
          }
        },
        function(error) {
          Notifications.message(error);
        }

      );
    }

    for (var i = 0; i < removeUsers.length; i++) {
      Office.removeUserFromOffice(removeUsers[i],vm.model.officeChange.id,
        function(ok) {
          vm.itemsModify = vm.itemsModify -1;
          if (vm.itemsModify == 0) {
            vm.filterUsers();
            vm.officeChange();
            Notifications.message("Se han guardados los cambios exitosamente");
          }
        },
        function(error) {
          Notifications.message(error);
        }

      );
    }
  }

  function cancel() {
    officeChange();
  }

}
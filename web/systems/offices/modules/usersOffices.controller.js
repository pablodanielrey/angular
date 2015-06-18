angular
    .module('mainApp')
    .controller('UsersOfficesController',UsersOfficesController);

UsersOfficesController.$inject = ['$scope','$location','Notifications', 'Office', 'Users'];

function UsersOfficesController($scope, $location, Notifications, Office, Users) {

  var vm = this;

  vm.model = {
    officeSelected: null,
    allOffices: [],
    users: []
  }

  vm.initialize = initialize;
  vm.initalizeAllUsers = initializeAllUsers;
  vm.loadOffices = loadOffices;

  function initialize() {
    vm.initalizeAllUsers();
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
      },
      function(error) {
        Notification.message(error);
      }
    );
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



}

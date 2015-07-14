angular
    .module('mainApp')
    .controller('AssistanceFailsFiltersCtrl',AssistanceFailsFiltersCtrl);


AssistanceFailsFiltersCtrl.$inject = ['$scope', '$timeout', 'Notifications', 'Assistance', 'Users', 'Utils', 'Session','filterFilter'];

function AssistanceFailsFiltersCtrl($scope, $timeout, Notifications, Assistance, Users, Utils, Session, filterFilter) {


  var vm = this;



  vm.model = {
    sessionUserId: null,
    searchUser: null,
    users: [],
    office: null,
    searchOffice: null,
    offices: [],
    filter:{
      begin:new Date(),
      end:new Date()
    }
  }

  vm.view = {
    displayListUser: false
  }

  vm.initialize = initialize;

  vm.initializeUsers = initializeUsers;
  vm.isDisplayListUser = isDisplayListUser;
  vm.displayListUser = displayListUser;
  vm.selectUser = selectUser;
  vm.hideListUser = hideListUser;

  vm.initializeOffices = initializeOffices;
  vm.isDisplayListOffice = isDisplayListOffice;
  vm.displayListOffice = displayListOffice;
  vm.loadOffices = loadOffices;
  vm.groupSelected = groupSelected;
  vm.hideListOffice = hideListOffice;

  vm.initializeFilter = initializeFilter;
  vm.correctDates = correctDates;


  /* ------------------------------------------
   * -------------- INICIALIZACION ------------
   * ------------------------------------------
   */

  function initialize() {
    var session = Session.getCurrentSession();
    vm.model.sessionUserId = session.user_id;

    vm.initializeUsers();
    vm.initializeOffices();
    vm.initializeFilter();
  }

  $scope.$on('$viewContentLoaded', function(event) {
    vm.initialize();
  });


  /* ------------------------------------------
   * --------------- USUARIOS -----------------
   * ------------------------------------------
   */

   function initializeUsers() {
     vm.model.searchUser = null;
     vm.model.users = [];
     vm.view.displayListUser = false;
     loadUsers();
   }

   function loadUser(id) {
     Users.findUser(id,
       function(user) {
         vm.model.users.push(user);
       },
       function (error) {
         Notifications.message(error);
       }
     );
   }

   function loadUsers() {
     Assistance.getUsersInOfficesByRole('autoriza',
      function(users) {
        vm.model.users = [];
        for (var i = 0; i < users.length; i++) {
          loadUser(users[i]);
        }
      },
      function(error) {
        Notifications.message(error);
      }
    );
   }

   function displayListUser() {
     vm.model.searchUser = null;
     vm.view.displayListUser = true;
   }

   function isDisplayListUser() {
     return vm.view.displayListUser;
   }

   function selectUser(user) {
     vm.model.user = user;
     vm.model.searchUser = vm.model.user.name + " " + vm.model.user.lastname;
     vm.view.displayListUser = false;
     vm.model.office = null;
     vm.model.searchOffice = null;
   }

   function hideListUser() {
     $timeout(function() {
       vm.view.displayListUser = false;
     },300);
   }


   /* ------------------------------------------
    * --------------- OFICINAS -----------------
    * ------------------------------------------
    */

    function initializeOffices() {
      vm.model.office = null,
      vm.model.offices = []
      vm.loadOffices();
      vm.view.displayListOffice = false;
    }

    function groupSelected(office) {
      vm.model.office = office;
      vm.model.searchOffice = vm.model.office.name;
      vm.view.displayListOffice = false;
      vm.model.user = null;
      vm.model.searchUser = null;
    }

    function isDisplayListOffice() {
      return vm.view.displayListOffice;
    }

    function loadOffices() {
      var userId = vm.model.sessionUserId;
      var tree = true;
      var role = 'autoriza';

      Assistance.getOfficesByUserRole(userId,role,tree,
        function(offices) {
          vm.model.offices = {};
          var rootNodes = searchRootNodes(offices);
          for (var i = 0; i < rootNodes.length; i++) {
            rootNodes[i].children = getChildren(rootNodes[i],offices);
          }
          if (rootNodes.length == 1) {
            vm.model.offices = rootNodes[0];
          } else {
            var root = {};
            root.name = '/';
            root.children = rootNodes;
            root.click = vm.groupSelected;
            vm.model.offices = root;
          }
        },
        function(error) {
          Notifications.message(error);
        }
      );
    }

    function getChildren(node,offices) {
      var childrens = [];
      for (var i = 0; i < offices.length; i++) {
        if (offices[i].parent == node.id) {
          childrens.push(offices[i]);
          offices[i].children = getChildren(offices[i], offices);
        }
      }
      return childrens;
    }

    function searchRootNodes(offices) {
      var rootNodes = [];
      for (var i = 0; i < offices.length; i++) {
        var node = offices[i];
        node.click = vm.groupSelected;
        if (node.parent == null) {
          rootNodes.push(node);
          continue;
        }
        var isRoot = true;
        for (var j = 0; j < offices.length; j++) {
          if (node.parent == offices[j].id) {
            isRoot = false;
            break;
          }
        }
        if (isRoot) {
          rootNodes.push(node);
        }
      }
      return rootNodes;
    }


    function displayListOffice() {
      vm.model.searchOffice = null;
      vm.view.displayListOffice = true;
    }

    function hideListOffice() {
      $timeout(function() {
        vm.view.displayListOffice = false;
      },300);
    }


    $scope.$watch('vm.model.searchOffice',function(newValue, oldValue) {
      // paso el tree a un array
      var officesArray = [];
      convertTreeToArray(vm.model.offices,officesArray);

      var filtered = [];
      if (newValue == null || newValue == '*' || newValue.trim() == '') {
        filtered = officesArray;
      } else {
        filtered = filterFilter(officesArray, {name:newValue});
      }
      for (var i = 0; i < officesArray.length; i++) {
        var office = officesArray[i];
        if (!include(filtered,office)) {
          office.hidden = true;
        } else {
          office.hidden = false;
        }
      }
    });

    function include(array,item) {
      var  index = array.indexOf(item);
      return index > -1;
    }

    function convertTreeToArray(node, array) {
      array.push(node);
      if (node.children == null || node.children.length == 0) {
        return;
      }
      for (var i = 0; i < node.children.length; i++) {
        convertTreeToArray(node.children[i],array);
      }
    }

    /* ------------------------------------------
     * ---------------- FILTROS -----------------
     * ------------------------------------------
     */

    function initializeFilter() {
      vm.model.filter = {};
      vm.correctDates();
    }

    function correctDates() {
      if(!vm.model.filter.begin) vm.model.filter.begin = new Date();
      vm.model.filter.begin.setHours(0);
      vm.model.filter.begin.setMinutes(0);
      vm.model.filter.begin.setSeconds(0);
      if((!vm.model.filter.end) || (vm.model.filter.end < vm.model.filter.begin)) vm.model.filter.end = new Date(vm.model.filter.begin);
      vm.model.filter.end.setHours(23);
      vm.model.filter.end.setMinutes(59);
      vm.model.filter.end.setSeconds(59);
    };

    $scope.$watch('vm.model.filter.begin', vm.correctDates);
    $scope.$watch('vm.model.filter.end', vm.correctDates);

    /* ------------------------------------------
     * ---------------- BUSCAR ------------------
     * ------------------------------------------
     */
}

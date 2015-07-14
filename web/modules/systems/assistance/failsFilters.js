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
    begin:null,
    end:null,
    searching:false,
    filter:{
      failsType:[],
      failTypeSelected:null,
      periodicities:[],
      periodicitySelected:null,
      count:1,
      hoursOperator:null,
      hoursOperators:[],
      hours:0,
      minutes:0
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

  vm.initializeDates = initializeDates;
  vm.correctDates = correctDates;

  vm.initializeFilter = initializeFilter;
  vm.initializeFailsType = initializeFailsType;
  vm.initializePeriodicity = initializePeriodicity;
  vm.initializeHoursOperator = initializeHoursOperator;
  vm.correctCount = correctCount;

  vm.search = search;

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

    vm.model.searching = false;
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
     * ---------------- FECHAS ------------------
     * ------------------------------------------
     */

    function initializeDates() {
      vm.correctDates();
    }

    function correctDates() {
      if(!vm.model.begin) vm.model.begin = new Date();
      vm.model.begin.setHours(0);
      vm.model.begin.setMinutes(0);
      vm.model.begin.setSeconds(0);
      if((!vm.model.end) || (vm.model.end < vm.model.begin)) vm.model.end = new Date(vm.model.begin);
      vm.model.end.setHours(23);
      vm.model.end.setMinutes(59);
      vm.model.end.setSeconds(59);
    };

    $scope.$watch('vm.model.begin', vm.correctDates);
    $scope.$watch('vm.model.end', vm.correctDates);
    $scope.$watch('vm.model.count', vm.correctCount);

    function correctCount() {
      if (vm.model.count < 1) {
        Notifications.message("No se pude ingresar un valor menor a 1");
        vm.model.count = 1;
      }
    }

    /* ------------------------------------------
     * ---------------- FILTROS -----------------
     * ------------------------------------------
     */

    function initializeFilter() {
      vm.model.filter = {};
      vm.initializeFailsType();
      vm.initializePeriodicity();
      vm.initializeHoursOperator();
      vm.model.filter.count = 1;
    }



    function initializeFailsType () {
      vm.model.filter.failTypeSelected = null;

      vm.model.filter.failsType = [];
      var t = {name:'No posee marcación',description:'No existe ninguna marcación para esa fecha',isHours:false};
      vm.model.filter.failsType.push(t);
      t = {name:'Sin horario de llegada',description:'Sin horario de llegada',isHours:false};
      vm.model.filter.failsType.push(t);
      t = {name:'Llegada tardía',description:'Llegada tardía',isHours:true};
      vm.model.filter.failsType.push(t);
      t = {name:'Sin horario de salida',description:'Sin horario de salida',isHours:false};
      vm.model.filter.failsType.push(t);
      t = {name:'Salida temprana',description:'Salida temprana',isHours:true};
      vm.model.filter.failsType.push(t);
    };

    function initializePeriodicity() {
      vm.model.filter.periodicities = ['Semanal','Mensual','Anual'];
      vm.model.filter.periodicitySelected = null;
    }

    function initializeHoursOperator() {
      vm.model.filter.hoursOperators = [];
      vm.model.filter.hoursOperators.push({value:'>',name:'Mayor a'});
      vm.model.filter.hoursOperators.push({value:'=',name:'Igual a'});
      vm.model.filter.hoursOperators.push({value:'<',name:'Menor a'});
      vm.model.filter.hoursOperator = vm.model.filter.hoursOperators[0];

      vm.model.filter.minutes = 0;
      vm.model.filter.hours = 0;
    }


    /* ------------------------------------------
     * ---------------- BUSCAR ------------------
     * ------------------------------------------
     */

     function search() {
       if (vm.model.user == null && vm.model.office == null) {
          Notifications.message("Necesita seleccionar un usuario o una oficina");
          return;
       }

       vm.model.searching = true;
       vm.model.assistanceFails = [];
       vm.correctDates();

       var users = [];
       if (vm.model.user != null) {
         users.push(vm.model.user)
       }

       var offices = [];
       if (vm.model.office != null) {
         offices.push(vm.model.office);
       }

       Assistance.getFailsByFilter(users, offices, vm.model.begin, vm.model.end, vm.model.filter,
         function(response) {
           for (var i = 0; i < response.response.length; i++) {

             var r = response.response[i];

             r.justification = {name:''};
             if ((r.fail.justifications != undefined) && (r.fail.justifications != null) && (r.fail.justifications.length > 0)) {
               var just = Utils.getJustification(r.fail.justifications[0].justification_id);
               just.begin = r.fail.justifications[0].begin;
               r.justification = just;
             }

             var date = new Date(r.fail.date);
             r.fail.dateFormat = Utils.formatDate(date);
             r.fail.dateExtend = Utils.formatDateExtend(date);
             r.fail.dayOfWeek = {};
             r.fail.dayOfWeek.name = Utils.getDayString(date);
             r.fail.dayOfWeek.number = date.getDay();



             if (r.fail.startSchedule || r.fail.endSchedule) {
               r.fail.dateSchedule = (r.fail.startSchedule) ? r.fail.startSchedule : r.fail.endSchedule;
               r.fail.dateSchedule = Utils.formatTime(new Date(r.fail.dateSchedule));
             }

             if (r.fail.start || r.fail.end) {
               r.fail.wh = (r.fail.start) ?  new Date(r.fail.start) : new Date(r.fail.end);
               r.fail.wh =  Utils.formatTime(r.fail.wh);
             }

             if (r.fail.seconds) {
               var hoursDiff = Math.floor((r.fail.seconds / 60) / 60);
               var minutesDiff = Math.floor((r.fail.seconds / 60) % 60);
               r.fail.diff = ('0' + hoursDiff).substr(-2) + ":" + ('0' + minutesDiff).substr(-2);
             }

             if (r.fail.whSeconds) {
               var hours = Math.floor((r.fail.whSeconds / 60) / 60);
               var minutes = Math.floor((r.fail.whSeconds / 60) % 60);
               r.fail.whs = ('0' + hours).substr(-2) + ":" + ('0' + minutes).substr(-2);
             } else {
               r.fail.whs = '00:00';
             }

             vm.model.assistanceFails.push(r);
           }
           vm.model.searching = false;
         },
         function(error) {
           vm.model.searching = false;
           Notifications.message(error);
         }
       );
     }
}

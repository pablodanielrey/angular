(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersListCtrl', MyOrdersListCtrl);

    MyOrdersListCtrl.$inject = ['$scope', '$location', '$window', '$timeout', '$filter', 'Login', 'Issues', 'Users', 'Offices', 'Files'];

    /* @ngInject */
    function MyOrdersListCtrl($scope, $location, $window, $timeout, $filter, Login, Issues, Users, Offices, Files) {
        var vm = this;

        vm.model = {
          userId: null, //usuario logueado
          users: [],
          issues: [],
          userOffices: [],
          privateTransport: null
        }

        ///////////////// barra de busqueda. header /////////////////////////////

        vm.model.header = {
            status:{
              open: true,
              working: true,
              paused: true,
              rejected: false,
              closed:false
            }
        }

        vm.headerStatusSelectAllToggle = headerStatusSelectAllToggle;
        vm.headerInvalidateIssuesCache = headerInvalidateIssuesCache;
        vm.headerSelectStatus = headerSelectStatus;
        vm.headerFindIssues = headerFindIssues;

        function headerFindIssues() {
          vm.view.style3 = vm.view.styles3[0];
          getMyIssues();
        }

        function headerSelectStatus() {
          if (vm.view.style3 == vm.view.styles3[5]) {
            vm.view.style3 = vm.view.styles3[0];
          } else {
            vm.view.style3 = vm.view.styles3[5];
          }
        }

        function headerInvalidateIssuesCache() {
          $window.sessionStorage.removeItem('assignedIssues');
          _persistHeaderFilters();
        }

        function _persistHeaderFilters() {
          $window.sessionStorage.setItem('hfo',JSON.stringify(vm.model.header.status.open));
          $window.sessionStorage.setItem('hfw',JSON.stringify(vm.model.header.status.working));
          $window.sessionStorage.setItem('hfp',JSON.stringify(vm.model.header.status.paused));
          $window.sessionStorage.setItem('hfr',JSON.stringify(vm.model.header.status.rejected));
          $window.sessionStorage.setItem('hfc',JSON.stringify(vm.model.header.status.closed));
        }

        function _loadHeaderFilters() {
            vm.model.header.status.open = JSON.parse($window.sessionStorage.getItem('hfo'));
            vm.model.header.status.working = JSON.parse($window.sessionStorage.getItem('hfw'));
            vm.model.header.status.paused = JSON.parse($window.sessionStorage.getItem('hfp'));
            vm.model.header.status.rejected = JSON.parse($window.sessionStorage.getItem('hfr'));
            vm.model.header.status.closed = JSON.parse($window.sessionStorage.getItem('hfc'));
        }

        function headerStatusSelectAllToggle() {
          headerInvalidateIssuesCache();
          var s = !vm.model.header.status.open;
          vm.model.header.status.open = s;
          vm.model.header.status.working = s;
          vm.model.header.status.paused = s;
          vm.model.header.status.rejected = s;
          vm.model.header.status.closed = s;
          _persistHeaderFilters();
        }

        function _getHeaderStatusFilter() {
          _loadHeaderFilters();
          var f = [];
          if (vm.model.header.status.open) {
            f.push(1);
          }
          if (vm.model.header.status.working) {
            f.push(2);
          }
          if (vm.model.header.status.paused) {
            f.push(7);
          }
          if (vm.model.header.status.rejected) {
            f.push(6);
          }
          if (vm.model.header.status.closed) {
            f.push(3);
          }
          return f;
        }

        ///////////////////////////////////////////////////////////////////////





        vm.view = {
          style1: '',
          styles1: ['','pantallaMensajeAlUsuario'],
          style2: '',
          styles2: ['', 'mensajeCargando'],
          style3: '',
          styles3: ['','mensajeCargando', 'mensajeError', 'mensajeEnviado', 'mensajePedidoCreado', 'seleccionarEstado'],

          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'rechazada', 'pausada'],
          statusSort: ['','abierta', 'enProgreso', 'pausada', 'rechazada', 'cerrada'],
          src: '#/myOrdersDetail/'
        }

        vm.sortStatus = sortStatus;
        vm.sortDate = sortDate;
        vm.loadUserOffices = loadUserOffices;

        function messageLoading() {
          vm.view.style1 = vm.view.styles1[1];
          vm.view.style2 = vm.view.styles2[1];
        }

        function closeMessage() {
          vm.view.style1 = vm.view.styles1[0];
          vm.view.style2 = vm.view.styles2[0];
        }

        function messageError(error) {
          vm.view.style3 = vm.view.styles3[1];
          vm.view.style4 = vm.view.styles4[2];
          $timeout(function() {
            vm.closeMessage();
          }, 2000);
        }


        $scope.$on('wamp.open', function(event, args) {
          vm.model.privateTransport = Login.getPrivateTransport();
          activate();
        });

        activate();


        function activate() {
          if (Login.getPrivateTransport() == null) {
            return;
          }
          vm.model.userId = Login.getCredentials().userId;
          vm.loadUserOffices(vm.model.userId);
          vm.model.issues = [];
          vm.model.users = [];
          vm.model.files = [];

          vm.view.reverseSortDate = true;
          vm.view.reverseSortStatus = true;
          registerEventManagers();

          getMyIssues();
        }


        function getMyIssues() {
          messageLoading();
          Issues.getMyIssues(_getHeaderStatusFilter()).then(
            function(issues) {
                for (var i = 0; i < issues.length; i++) {
                  var dateStr = issues[i].start;
                  issues[i].date = new Date(dateStr);

                  // obtengo la posicion de ordenacion del estado
                  var status = vm.view.status[issues[i].statusId];
                  issues[i].statusPosition = vm.view.statusSort.indexOf(status);

                  loadUser(issues[i].userId);
                  loadUser(issues[i].creatorId);
                }
                $timeout(function() {
                  vm.model.issues = issues;
                  closeMessage();
                  sortIssues();
                });
            },
            function(err) {
              messageError(error);
            }
          );
        }


        //////////////////////// ORDENAMIENTO DEL LISTADO //////////////////////////

        /*
          Dispara la ordenación del listado.
        */
        function sortIssues() {
          var order = $window.sessionStorage.getItem('listSort');
          if (order == null) {
            order = ['start', '-priority', 'statusPosition'];
            $window.sessionStorage.setItem('listSort', JSON.stringify(order));
          } else {
            order = JSON.parse(order);
          }
          vm.model.issues = $filter('orderBy')(vm.model.issues, order, false);
        }

        /*
          retorna el valor de orden inverso o order normal. y almacena el inverso.
          solo se usa cuando se clickea el ordenamiento explícitamente.
          no cuando se ordena el listado.
        */
        function _processSortRev() {
          var rev = $window.sessionStorage.getItem('reverseSort');
          if (rev == null) {
            rev = false;
            $window.sessionStorage.setItem('reverseSort', JSON.stringify(!rev));
          } else {
            rev = JSON.parse(rev);
          }

          // almaceno el orden a inverso.
          if (rev) {
            $window.sessionStorage.setItem('reverseSort', JSON.stringify(!rev));
          } else {
            $window.sessionStorage.setItem('reverseSort', JSON.stringify(!rev));
          }

          return rev;
        }

        function sortDate() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ['start', '-priority', 'statusPosition'];
          } else {
            order = ['-start', '-priority', 'statusPosition'];
          }
          $window.sessionStorage.setItem('listSort', JSON.stringify(order));
          sortIssues();

          /*
          vm.view.sortedBy = 'date';
          vm.view.reverseSortDate = !vm.view.reverseSortDate;
          vm.view.reverseSortStatus = true;
          vm.view.reverseSortPriority = false;
          orderByDate();
          */
        }


        function sortStatus() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ['statusPosition', '-priority', 'start'];
          } else {
            order = ['-statusPosition', '-priority', '-start'];
          }
          $window.sessionStorage.setItem('listSort', JSON.stringify(order));
          sortIssues();

          /*
          vm.view.sortedBy = 'status';
          vm.view.reverseSortStatus = !vm.view.reverseSortStatus;
          vm.view.reverseSortDate = true;
          vm.view.reverseSortPriority = false;
          orderByStatus();
          */
        }


        function sortPriority() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ['-priority', '-start', 'statusPosition'];
          } else {
            order = ['priority', '-start', 'statusPosition'];
          }
          $window.sessionStorage.setItem('listSort', JSON.stringify(order));
          sortIssues();

          /*
          vm.view.sortedBy = 'priority';
          vm.view.reverseSortPriority = !vm.view.reverseSortPriority;
          vm.view.reverseSortDate = true;
          vm.view.reverseSortStatus = true;
          orderByPriority();
          */
        }

        ///////////////////////////////////////////////////////////




        //***** cargar usuario en vm.model.users *****
        function loadUser(userId) {
          if (!userId || userId == '') return;

          if (vm.model.users[userId] == null) {
            Users.findById([userId]).then(
              function(users) {
                $timeout(function() {
                  vm.model.users[userId] = users[0];
                });
              }
            );
          }
        }



      function registerEventManagers() {
        Issues.subscribe('issues.issue_created_event', function(params) {
          var issueId = params[0];
          var authorId = params[1];
          var fromOfficeId = params[2];
          var officeId = params[3];
          if (authorId == vm.model.userId || vm.model.userOffices[fromOfficeId] != null) {
              Issues.findById(issueId).then(
                function(issue) {
                  if (issue != null) {
                    var dateStr = issue.start;
                    issue.date = new Date(dateStr);

                    // obtengo la posicion de ordenacion del estado
                    var item = vm.view.status[issue.statusId];
                    issue.statusPosition = vm.view.statusSort.indexOf(item);

                    loadUser(issue.userId);
                    loadUser(issue.creatorId);
                    $timeout(function() {
                      vm.model.issues.push(issue);
                      sortIssues();
                    });
                  }
                },
                function(error) {
                  messageError()
                }
              )
          }
        });

        Issues.subscribe('issues.updated_event', function(params) {
          Issues.updateIssue(params[0], params[1], params[2]);
          var id = params[0];
          for (var i = 0; i < vm.model.issues.length; i++) {
            if (id == vm.model.issues[i].id) {
              $timeout(function() {
                vm.model.issues[i].statusId = params[1];
                vm.model.issues[i].priority = params[2];
              });
              break;
            }
          }
        });

      }

    function loadUserOffices(userId) {
      vm.model.userOffices = [];
      Offices.getOfficesByUser(userId, false).then(
        function(ids) {
          if (ids == null || ids.length <= 0) {
            return;
          }
          Offices.findById(ids).then(
            function(offices) {
              $timeout(function() {
                vm.model.userOffices = [];
                if (offices == null || offices.length <= 0) {
                    return;
                }
                for (var i = 0; i < offices.length; i++) {
                  vm.model.userOffices[offices[i].id] = offices[i];
                }
              });
            }, function(error) {
              messageError(error);
            }
          )
        }, function(error) {
          messageError(error);
        }
      );
    }
  }
})();

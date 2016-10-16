(function() {
    'use strict';

    angular
        .module('issues')
        .controller('OrdersListCtrl', OrdersListCtrl);

    OrdersListCtrl.$inject = ['$scope', '$location', 'Issues', 'Users', '$filter', 'Login', 'Offices', '$timeout', '$window', '$q'];

    /* @ngInject */
    function OrdersListCtrl($scope, $location, Issues, Users, $filter, Login, Offices, $timeout, $window, $q) {
        var vm = this;

        vm.model = {
          userId: null, //usuario logueado
          users: [],
          issues: [],
          userOffices: []
        }



        ///////////////// barra de busqueda. header /////////////////////////////

        vm.model.header = {
            status:{
              open: true,
              working: true,
              paused: true,
              rejected: false,
              closed:false
            },
            userOffices: [],
            offices: []
        }

        vm.headerStatusSelectAllToggle = headerStatusSelectAllToggle;
        vm.headerAreaSelectAllToggle = headerAreaSelectAllToggle;
        vm.headerOfficesSelectAllToggle = headerOfficesSelectAllToggle;
        vm.headerInvalidateIssuesCache = headerInvalidateIssuesCache;
        vm.headerSelectTo = headerSelectTo;
        vm.headerSelectStatus = headerSelectStatus;
        vm.headerSelectFrom = headerSelectFrom;
        vm.headerFindIssues = headerFindIssues;

        function headerFindIssues() {
          vm.view.style3 = vm.view.styles3[0];
          loadIssues();
        }

        function headerSelectStatus() {
          if (vm.view.style3 == vm.view.styles3[1]) {
            vm.view.style3 = vm.view.styles3[0];
          } else {
            vm.view.style3 = vm.view.styles3[1];
          }
        }

        function headerSelectTo() {
          if (vm.view.style3 == vm.view.styles3[2]) {
            vm.view.style3 = vm.view.styles3[0];
          } else {
            vm.view.style3 = vm.view.styles3[2];
          }
        }

        function headerSelectFrom() {
          if (vm.view.style3 == vm.view.styles3[3]) {
            vm.view.style3 = vm.view.styles3[0];
          } else {
            vm.view.style3 = vm.view.styles3[3];
          }
        }

        function headerInvalidateIssuesCache() {
          $window.sessionStorage.removeItem('assignedIssues');
          _persistHeaderFilters();
        }

        function headerAreaSelectAllToggle() {
          for (var i = 0; i < vm.model.header.userOffices.length; i++) {
            var a = vm.model.header.userOffices[i];
            a.active = !a.active;
          }
          _persistHeaderFilters();
        }

        function headerOfficesSelectAllToggle() {
          for (var i = 0; i < vm.model.header.offices.length; i++) {
            var a = vm.model.header.offices[i];
            a.active = !a.active;
          }
          _persistHeaderFilters();
        }

        function headerStatusSelectAllToggle() {
          var s = !vm.model.header.status.open;
          vm.model.header.status.open = s;
          vm.model.header.status.working = s;
          vm.model.header.status.paused = s;
          vm.model.header.status.rejected = s;
          vm.model.header.status.closed = s;
          _persistHeaderFilters();
        }

        function _processHeaderToOffices(offices) {
          if (offices == null) {
            return;
          }
          vm.model.header.userOffices = offices;
          for (var i = 0; i < vm.model.header.userOffices.length; i++) {
            vm.model.header.userOffices[i].active = true;
          }
        }

        function headerLoadOffices() {
          var d = $q.defer();

          Offices.findAll().then(Offices.findById).then(
            function(off) {
              vm.model.header.offices = off;
              d.resolve();
            });

          return d.promise;
        }

        function _getHeaderToFilter() {
          _loadHeaderFilters();
          var f = [];
          for (var i = 0; i < vm.model.header.userOffices.length; i++) {
            if (vm.model.header.userOffices[i].active) {
              f.push(vm.model.header.userOffices[i].id);
            }
          }
          return f;
        }

        function _getHeaderFromFilter() {
          _loadHeaderFilters();
          var f = [];
          for (var i = 0; i < vm.model.header.offices.length; i++) {
            if (vm.model.header.offices[i].active) {
              f.push(vm.model.header.offices[i].id);
            }
          }
          return f;
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


        function _persistHeaderFilters() {
          $window.sessionStorage.setItem('hfo',JSON.stringify(vm.model.header.status.open));
          $window.sessionStorage.setItem('hfw',JSON.stringify(vm.model.header.status.working));
          $window.sessionStorage.setItem('hfp',JSON.stringify(vm.model.header.status.paused));
          $window.sessionStorage.setItem('hfr',JSON.stringify(vm.model.header.status.rejected));
          $window.sessionStorage.setItem('hfc',JSON.stringify(vm.model.header.status.closed));

          for (var i = 0; i < vm.model.header.offices.length; i++) {
            $window.sessionStorage.setItem('hFromOffices_' + vm.model.header.offices[i].id, JSON.stringify(vm.model.header.offices[i].active));
          }

          for (var i = 0; i < vm.model.header.userOffices.length; i++) {
            $window.sessionStorage.setItem('hUserOffices_' + vm.model.header.userOffices[i].id, JSON.stringify(vm.model.header.userOffices[i].active));
          }
        }

        function _loadHeaderFilters() {
            vm.model.header.status.open = JSON.parse($window.sessionStorage.getItem('hfo'));
            vm.model.header.status.working = JSON.parse($window.sessionStorage.getItem('hfw'));
            vm.model.header.status.paused = JSON.parse($window.sessionStorage.getItem('hfp'));
            vm.model.header.status.rejected = JSON.parse($window.sessionStorage.getItem('hfr'));
            vm.model.header.status.closed = JSON.parse($window.sessionStorage.getItem('hfc'));

            for (var i = 0; i < vm.model.header.offices.length; i++) {
              var id = vm.model.header.offices[i].id;
              var a = JSON.parse($window.sessionStorage.getItem('hFromOffices_' + id));
              vm.model.header.offices[i].active = a;
            }

            for (var i = 0; i < vm.model.header.userOffices.length; i++) {
              var id = vm.model.header.userOffices[i].id;
              var a = JSON.parse($window.sessionStorage.getItem('hUserOffices_' + id));
              vm.model.header.userOffices[i].active = a;
            }
        }

        ///////////////////////////////////////////////////////////////////////



        vm.view = {
          style1: '',
          styles1: ['','pantallaMensajeAlUsuario'],
          style2: '',
          styles2: ['', 'mensajeCargando', 'mensajeError'],
          style3: '',
          styles3: ['','seleccionarEstado','seleccionarAreas','SeleccionarOficinas'],

          search: '',
          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'cerrada', 'rechazada', 'pausada'],
          statusSort: ['','abierta', 'enProgreso', 'pausada', 'rechazada', 'cerrada'],
          priorities: ['baja', 'normal', 'alta', 'alta', 'alta'], //solo se maneja el estilo alta, si esta como urgente o inmediata se lo toma solo como alta
          src: '#/ordersDetail/'
        }

        vm.loadIssues = loadIssues;
        vm.sortDate = sortDate;
        vm.sortStatus = sortStatus;
        vm.sortPriority = sortPriority;
        vm.loadUser = loadUser;

        vm.closeMessage = closeMessage;
        vm.messageLoading = messageLoading;
        vm.messageError = messageError;

        vm.loadUserOffices = loadUserOffices;


        $scope.$on('wamp.open', function(event, args) {
          activate();
        });

        activate();

        function preLoad() {

        }


        function activate() {
          if (Login.getPrivateTransport() == null) {
            return;
          }

          vm.model.userId = Login.getCredentials().userId;
          vm.loadUserOffices(vm.model.userId);
          vm.view.reverseSortDate = true;
          vm.view.reverseSortStatus = true;
          vm.view.reverseSortPriority = false;
          vm.view.search = '';
          registerEventManagers();
          headerLoadOffices().then(function() {
            loadIssues();
          });
        }

        function loadIssues() {
          vm.model.issues = [];
          vm.messageLoading();
          Issues.getAssignedIssues(_getHeaderStatusFilter(), _getHeaderFromFilter(), _getHeaderToFilter()).then(
            function(issues) {
              var users = [];
              var uid = null;
              for (var i = 0; i < issues.length; i++) {
                var dateStr = issues[i].start;
                issues[i].date = new Date(dateStr);

                // obtengo la posicion de ordenacion del estado
                var item = vm.view.status[issues[i].statusId];
                issues[i].statusPosition = vm.view.statusSort.indexOf(item);

                uid = issues[i].userId;
                if (vm.model.users[uid] == null) {
                  users.push(uid);
                }
                uid = issues[i].creatorId
                if (vm.model.users[uid] == null) {
                  users.push(uid);
                }
              }
              if (users.length > 0) {
                loadUsers(users);
              }
              $timeout(function() {
                vm.model.issues = issues;
                vm.closeMessage();
                sortIssues();
              });
            },
            function(error) {
              $timeout(function() {
                vm.messageError(error);
              });
            }
          );
        }

        function messageError(error) {
          vm.view.style1 = vm.view.styles1[1];
          vm.view.style2 = vm.view.styles2[2];
          $timeout(function() {
            vm.closeMessage();
          }, 3000);
        }

        function closeMessage() {
          vm.view.style1 = vm.view.styles1[0];
          vm.view.style2 = vm.view.styles2[0];
        }

        function messageLoading() {
          vm.view.style1 = vm.view.styles1[1];
          vm.view.style2 = vm.view.styles2[1];
        }

        //////////////// carga de usuarios refereciados por los issues ////////////////

        function loadUser(userId) {
          if (userId == null || userId == '') {
            return
          }
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

        function loadUsers(userIds) {
          Users.findById(userIds).then(
            function(users) {
              $timeout(function() {
                for (var i = 0; i < users.length; i++) {
                  vm.model.users[users[i].id] = users[i];
                }
              });
            }
          );
        }

        ///////////////////////////////////////////////////
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


        ////////////////////////////////////////////////////////////////////

        function registerEventManagers() {
          Issues.subscribe('issues.issue_created_event', function(params) {
            var issueId = params[0];
            var authorId = params[1];
            var fromOfficeId = params[2];
            var officeId = params[3];
            if (vm.model.userOffices[officeId] != null) {
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
          Offices.findByUser(userId, true).then(Offices.findByIds).then(
              function(offices) {
                $timeout(function() {
                    vm.model.userOffices = [];
                    if (offices == null || offices.length <= 0) {
                        return;
                    }
                    for (var i = 0; i < offices.length; i++) {
                      vm.model.userOffices[offices[i].id] = offices[i];
                    }

                    // esto carga en el header el tema de las oficinas de destino del pedido
                    _processHeaderToOffices(offices);

                });
              }, function(error) {
                $timeout(function() {
                  vm.messageError(error);
                });
              });
        }

    }
})();

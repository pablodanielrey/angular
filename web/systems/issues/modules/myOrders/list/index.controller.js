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
        }

        function headerStatusSelectAllToggle() {
          headerInvalidateIssuesCache();
          var s = !vm.model.header.status.open;
          vm.model.header.status.open = s;
          vm.model.header.status.working = s;
          vm.model.header.status.paused = s;
          vm.model.header.status.rejected = s;
          vm.model.header.status.closed = s;
        }

        function _getHeaderStatusFilter() {
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
          reverseSortDate: true,
          reverseSortStatus: true,
          sortedBy: 'status',
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
                  sortStatus();
                  closeMessage();
                });
            },
            function(err) {
              messageError(error);
            }
          );
        }




        function sortStatus() {
          vm.view.reverseSortStatus = !vm.view.reverseSortStatus;
          vm.view.sortedBy = 'status';
          vm.view.reverseSortDate = true;
          orderByStatus();
        }

        function orderByStatus() {
          if (vm.view.reverseSortStatus) {
            vm.model.issues = $filter('orderBy')(vm.model.issues, ['-statusPosition', '-start'], false);
          } else {
            vm.model.issues = $filter('orderBy')(vm.model.issues, ['statusPosition', '-start'], false);
          }

        }

        function sortDate() {
          vm.view.reverseSortDate = !vm.view.reverseSortDate;
          vm.view.sortedBy = 'date';
          vm.view.reverseSortStatus = true;
          orderByDate();
        }

        function orderByDate() {
          if (vm.view.reverseSortDate) {
            vm.model.issues = $filter('orderBy')(vm.model.issues, ['start', 'statusPosition'], false);
          } else {
            vm.model.issues = $filter('orderBy')(vm.model.issues, ['-start', 'statusPosition'], false);
          }
        }


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
                    });
                    if (vm.view.sortedBy == 'status') {
                      orderByStatus();
                    } else {
                      orderByDate();
                    }
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

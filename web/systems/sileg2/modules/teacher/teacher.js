(function() {
    'use strict';

    angular
        .module('sileg')
        .controller('TeacherCtrl', TeacherCtrl);

    TeacherCtrl.$inject = ['$scope', '$location', '$timeout', '$window', '$q', 'Sileg'];

    /* @ngInject */
    function TeacherCtrl($scope, $location, $timeout, $window, $q, Sileg) {
        var vm = this;

        vm.model = {} //variables del controlador
        vm.view = {} //variables de la vista

        function modelMethod(){} //metodo accedido desde el controlador

        vm.viewMethod = viewMethod; //metodo accedido desde la vista
        function method(){};

        function activate(){} //metodo de activacion
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
          var order = $window.localStorage.getItem('listSort');
          if (order == null) {
            order = ['start', '-priority', 'statusPosition'];
            $window.localStorage.setItem('listSort', JSON.stringify(order));
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
          var rev = $window.localStorage.getItem('reverseSort');
          if (rev == null) {
            rev = false;
            $window.localStorage.setItem('reverseSort', JSON.stringify(!rev));
          } else {
            rev = JSON.parse(rev);
          }

          // almaceno el orden a inverso.
          if (rev) {
            $window.localStorage.setItem('reverseSort', JSON.stringify(!rev));
          } else {
            $window.localStorage.setItem('reverseSort', JSON.stringify(!rev));
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
          $window.localStorage.setItem('listSort', JSON.stringify(order));
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
          $window.localStorage.setItem('listSort', JSON.stringify(order));
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
          $window.localStorage.setItem('listSort', JSON.stringify(order));
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

(function() {
    'use strict';

    angular
        .module('issues')
        .controller('OrdersListCtrl', OrdersListCtrl);

    OrdersListCtrl.$inject = ['$scope', '$location', 'Issues', 'Users', '$filter', 'Login', 'Offices'];

    /* @ngInject */
    function OrdersListCtrl($scope, $location, Issues, Users, $filter, Login, Offices) {
        var vm = this;

        vm.model = {
          userId: null, //usuario logueado
          users: [],
          issues: [],
          userOffices: []
        }

        vm.view = {
          style1: '',
          styles1: ['','pantallaMensajeAlUsuario'],
          style2: '',
          styles2: ['', 'mensajeCargando', 'mensajeError'],

          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'cerrada', 'rechazada', 'pausada'],
          statusSort: ['','abierta', 'enProgreso', 'pausada', 'rechazada', 'cerrada'],
          priorities: ['baja', 'normal', 'alta', 'alta', 'alta'], //solo se maneja el estilo alta, si esta como urgente o inmediata se lo toma solo como alta
          reverseSortDate: false,
          reverseSortStatus: false,
          reverseSortPriority: true
        }

        vm.sortDate = sortDate;
        vm.sortStatus = sortStatus;
        vm.sortPriority = sortPriority;
        vm.loadUser = loadUser;

        vm.closeMessage = closeMessage;
        vm.messageLoading = messageLoading;
        vm.messageError = messageError;

        vm.viewDetail = viewDetail;
        vm.loadUserOffices = loadUserOffices;


        activate();

        function activate() {
          vm.model.userId = Login.getCredentials().userId;
          vm.loadUserOffices(vm.model.userId);
          vm.view.reverseSortDate = false;
          vm.view.reverseSortStatus = false;
          vm.view.reverseSortDate = false;
          vm.view.reverseSortPriority = true;
          registerEventManagers();
          loadIssues();
        }

        function  loadIssues() {
          vm.model.issues = [];
          vm.messageLoading();
          Issues.getAssignedIssues().then(
            function(issues) {
              for (var i = 0; i < issues.length; i++) {
                var dateStr = issues[i].start;
                issues[i].date = new Date(dateStr);

                // obtengo la posicion de ordenacion del estado
                var item = vm.view.status[issues[i].statusId];
                issues[i].statusPosition = vm.view.statusSort.indexOf(item);

                vm.loadUser(issues[i].userId);
                vm.loadUser(issues[i].creatorId);
              }
              vm.model.issues = issues;
              vm.sortStatus();
              vm.closeMessage();
            },
            function(error) {
              vm.messageError(error);
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

        function loadUser(userId) {
          if (userId == null || userId == '') {
            return
          }
          if (vm.model.users[userId] == null) {
            Users.findById([userId]).then(
              function(users) {
                vm.model.users[userId] = users[0];
              }
            );
          }
        }

        function sortDate() {
          vm.view.reverseSortStatus = false;
          vm.view.reverseSortPriority = true;
          vm.model.issues = $filter('orderBy')(vm.model.issues, ['start', '-priority', 'statusPosition'], vm.view.reverseSortDate);
          vm.view.reverseSortDate = !vm.view.reverseSortDate;
        }

        function sortStatus() {
          vm.view.reverseSortDate = false;
          vm.view.reverseSortPriority = true;
          vm.model.issues = $filter('orderBy')(vm.model.issues, ['statusPosition', '-priority', 'start'], vm.view.reverseSortStatus);
          vm.view.reverseSortStatus = !vm.view.reverseSortStatus;
        }

        function sortPriority() {
          vm.view.reverseSortDate = false;
          vm.view.reverseSortStatus = false;
          vm.model.issues = $filter('orderBy')(vm.model.issues, ['priority', 'start', 'statusPosition'], vm.view.reverseSortPriority);
          vm.view.reverseSortPriority = !vm.view.reverseSortPriority;
        }


        function viewDetail(issueId) {
          $location.path('/ordersDetail/' + issueId);
        }


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
                      vm.model.issues.push(issue);
                    }
                  },
                  function(error) {
                    messageError()
                  }
                )
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
                  vm.model.userOffices = [];
                  if (offices == null || offices.length <= 0) {
                      return;
                  }
                  for (var i = 0; i < offices.length; i++) {
                    vm.model.userOffices[offices[i].id] = offices[i];
                  }
                }, function(error) {
                  vm.messageError(error);
                }
              )
            }, function(error) {
              vm.messageError(error);
            }
          );
        }

    }
})();

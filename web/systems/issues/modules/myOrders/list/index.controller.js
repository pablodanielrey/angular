(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersListCtrl', MyOrdersListCtrl);

    MyOrdersListCtrl.$inject = ['$scope', '$location', '$timeout', '$filter', 'Login', 'Issues', 'Users', 'Offices', 'Files'];

    /* @ngInject */
    function MyOrdersListCtrl($scope, $location, $timeout, $filter, Login, Issues, Users, Offices, Files) {
        var vm = this;

        vm.model = {
          userId: null, //usuario logueado
          users: [],
          issues: []
        }

        vm.view = {
          style1: '',
          styles1: ['','pantallaMensajeAlUsuario'],
          style2: '',
          styles2: ['', 'mensajeCargando'],

          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'rechazada', 'pausada'],
          statusSort: ['','abierta', 'enProgreso', 'pausada', 'rechazada', 'cerrada'],
          reverseSortDate: false,
          reverseSortStatus: false
        }

        vm.sortStatus = sortStatus;
        vm.sortDate = sortDate;
        vm.viewDetail = viewDetail;

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


        activate();


        function activate() {
          vm.model.userId = Login.getCredentials().userId;
          vm.model.issues = [];
          vm.model.users = [];
          vm.model.files = [];

          vm.view.reverseSortDate = false;
          vm.view.reverseSortStatus = false;

          getMyIssues();
        }


        function getMyIssues() {
          messageLoading();
          Issues.getMyIssues().then(
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
                vm.model.issues = issues;
                sortStatus();
                closeMessage();
            },
            function(err) {
              messageError(error);
            }
          );
        }




        function sortStatus() {
          vm.view.reverseSortDate = false;
          vm.model.issues = $filter('orderBy')(vm.model.issues, ['statusPosition', 'start'], vm.view.reverseSortStatus);
          vm.view.reverseSortStatus = !vm.view.reverseSortStatus;
        }

        function sortDate() {
          vm.view.reverseSortStatus = false;
          vm.model.issues = $filter('orderBy')(vm.model.issues, ['start', 'statusPosition'], vm.view.reverseSortDate);
          vm.view.reverseSortDate = !vm.view.reverseSortDate;
        }


        //***** cargar usuario en vm.model.users *****
        function loadUser(userId) {
          if (!userId || userId == '') return;

          if (vm.model.users[userId] == null) {
            Users.findById([userId]).then(
              function(users) {
                vm.model.users[userId] = users[0];
              }
            );
          }
        }

        function viewDetail(issueId) {
            $location.path('/myOrdersDetail/' + issueId);
        }



        function registerEventManagers() {
          Issues.subscribe('issues.issue_created_event', function(params) {
            var issueId = params[0];
            var authorId = params[1];
            var fromOfficeId = params[2];
            var officeId = params[3];
            if (authorId == vm.model.userId || vm.model.userOffices.indexOf(officeId) > -1) {
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
    }
})();

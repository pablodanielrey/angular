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
              vm.messageError(error);
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


    }
})();

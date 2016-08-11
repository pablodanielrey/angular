(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersListCtrl', MyOrdersListCtrl);

    MyOrdersListCtrl.$inject = ['$scope', '$timeout', '$filter', 'Login', 'Issues', 'Users', 'Offices', 'Files'];

    /* @ngInject */
    function MyOrdersListCtrl($scope, $timeout, $filter, Login, Issues, Users, Offices, Files) {
        var vm = this;

        vm.model = {
          userId: null, //usuario logueado
          users: [],
          issues: []
        }

        vm.view = {

          style3: '',
          styles3: ['','pantallaMensajeAlUsuario'],
          style4: '',
          styles4: ['', 'mensajeCargando'],

          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'rechazada', 'pausada'],
          statusSort: ['','abierta', 'enProgreso', 'pausada', 'rechazada', 'cerrada'],
          reverseSortDate: false,
          reverseSortStatus: false
        }


        vm.closeMessage = closeMessage;
        vm.getMyIssues = getMyIssues;
        vm.initializeModel = initializeModel;
        vm.initializeView = initializeView;
        vm.messageLoading = messageLoading;
        vm.sortStatus = sortStatus;

        function messageLoading() {
          vm.view.style3 = vm.view.styles3[1];
          vm.view.style4 = vm.view.styles4[1];
        }

        function closeMessage() {
          vm.view.style3 = vm.view.styles3[0];
          vm.view.style4 = vm.view.styles4[0];
        }



        activate();


        function activate() {
          vm.model.userId = Login.getCredentials().userId;
          vm.initializeModel();

        }


        function getMyIssues() {
          vm.messageLoading();
          Issues.getMyIssues().then(
            function(issues) {
                for (var i = 0; i < issues.length; i++) {
                  var dateStr = issues[i].start;
                  issues[i].date = new Date(dateStr);

                  // obtengo la posicion de ordenacion del estado
                  var item = vm.view.status[issues[i].statusId];
                  issues[i].statusPosition = vm.view.statusSort.indexOf(item);

                }
                vm.model.issues = issues;
                vm.sortStatus();
                vm.closeMessage();
            },
            function(err) {
              vm.messageError(error);
            }
          );
        }


        function initializeModel() {
          vm.model.issues = [];
          vm.model.users = [];
          vm.model.files = [];
          vm.getMyIssues();
        }

        function initializeView() {
          vm.view.reverseSortDate = false;
          vm.view.reverseSortStatus = false;
        }

        function sortStatus() {
          vm.view.reverseSortDate = false;
          vm.model.issues = $filter('orderBy')(vm.model.issues, ['statusPosition', 'start'], vm.view.reverseSortStatus);
          vm.view.reverseSortStatus = !vm.view.reverseSortStatus;
        }





    }
})();

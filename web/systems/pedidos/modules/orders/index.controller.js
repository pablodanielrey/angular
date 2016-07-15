(function() {
    'use strict';

    angular
        .module('mainApp')
        .controller('OrdersCtrl', OrdersCtrl);

    OrdersCtrl.$inject = ['$scope', '$timeout', '$filter', 'Login', 'Issue', 'Users'];

    /* @ngInject */
    function OrdersCtrl($scope, $timeout, $filter,  Login, Issue, Users) {
        var vm = this;

        // variables del modelo
        vm.model = {
          userId: '',
          users: [],
          issues: []
        }

        // variables de la vista
        vm.view = {
          style: '',
          styles: ['', 'pantallaDetallePedido', 'pantallaMensaje', 'pantallaNuevoPedido', 'buscarPedidos'],
          style2: '',
          styles2: ['', 'buscarOficina', 'buscarArea', 'buscarConsulta', 'buscarUsuario', 'buscarOficinaDeUsuario', 'seleccionarEstado', 'seleccionarPrioridad'],
          style3: '',
          styles3: ['','pantallaMensajeAlUsuario'],
          style4: '',
          styles4: ['', 'mensajeCargando', 'mensajeError', 'mensajeEnviado', 'mensajePedidoCreado'],
          status: ['','abierta', 'enProgreso', 'cerrada', 'pausada', 'rechazada'],
          statusSort: ['','abierta', 'enProgreso', 'pausada', 'rechazada', 'cerrada'],
          priorities: ['baja', 'normal', 'alta'],
          reverseSortDate: false,
          reverseSortStatus: false,
          reverseSortPriority: true
        }

        // métodos
        vm.initializeModel = initializeModel;
        vm.initializeView = initializeView;

        vm.closeMessage = closeMessage;
        vm.messageLoading = messageLoading;
        vm.messageError = messageError;
        vm.messageSending = messageSending;
        vm.messageCreated = messageCreated;

        vm.loadIssues = loadIssues;
        vm.loadUser = loadUser;

        vm.createIssue = createIssue;
        vm.createComment = createComment;
        vm.selectIssue = selectIssue;

        vm.getPriority = getPriority;
        vm.getDate = getDate;
        vm.getDiffDay = getDiffDay;
        vm.getStatus = getStatus;
        vm.getFromOffice = getFromOffice;
        vm.getOffice = getOffice;
        vm.getFullName = getFullName;
        vm.getCreator = getCreator;

        vm.sortDate = sortDate;
        vm.sortStatus = sortStatus;
        vm.sortPriority = sortPriority;

        activate();

        function activate() {
          vm.model.userId = '';
          vm.initializeView();
          Login.getSessionData()
            .then(function(s) {
                vm.model.userId = s.user_id;
                vm.initializeModel();
            }, function(err) {
              $scope.$apply(function() {
                vm.messageError(err);
              })
            });
        }

/* ************************************************************************ */
/* ********************** INICIALIZACION ********************************** */
/* ************************************************************************ */

        function initializeView() {
          vm.view.style = vm.view.styles[0];
          vm.view.style2 = vm.view.styles2[0];
          vm.view.style3 = vm.view.styles3[0];
          vm.view.style4 = vm.view.styles4[0];
        }

        function initializeModel() {
          vm.loadIssues();
        }

/* ************************************************************************ */
/* ******************** CONSULTAS AL MODELO ******************************* */
/* ************************************************************************ */

      function  loadIssues() {
        vm.model.issues = [];
        vm.messageLoading();
        Issue.getAssignedIssues().then(
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
            $scope.$apply(function() {
              vm.closeMessage();
            })
          },
          function(error) {
            $scope.$apply(function() {
              vm.messageError(error);
            })
          }
        );
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

/* ************************************************************************ */
/* ************************ NAVEGACION ************************************ */
/* ************************************************************************ */

      function selectIssue(issue) {
        vm.view.style = vm.view.styles[1];
        vm.model.selectedIssue = issue;
      }

      function cancel() {
        vm.model.selectedIssue = null;
        vm.view.style = vm.view.styles[0];
      }

      function createIssue() {
        vm.view.style = vm.view.styles[3];
      }

      function createComment() {
        vm.view.style = vm.view.styles[2];
      }


/* ************************************************************************ */
/* ********************* FORMATO DE DATOS ********************************* */
/* ************************************************************************ */

      function getPriority(issue) {
        var p = (issue.priority > 2) ? 2 : issue.priority - 1;
        return vm.view.priorities[p];
      }

      function getDate(issue) {
        if (issue == null) {
          return '';
        }
        var date = ('date' in issue) ? issue.date : new Date(issue.start);
        return date;
      }

      function _setInitDay(date) {
        date.setHours(0);
        date.setMinutes(0);
        date.setSeconds(0);
        date.setMilliseconds(0);
      }

      function getDiffDay(issue) {
        if (issue == null) {
          return '';
        }
        var date = ('date' in issue) ? new Date(issue.date) : new Date(issue.start);
        var now = new Date();
        _setInitDay(date);
        _setInitDay(now);
        var diff = now - date;
        var days = Math.floor(diff / (1000 * 60 * 60 * 24));
        return (days == 0) ? 'Hoy' : (days == 1) ? 'Ayer' : 'Hace ' + days + ' días'
      }

      function getStatus(issue) {
        if (issue == null) {
          return '';
        }
        return vm.view.status[issue.statusId];
      }

      function getFromOffice(issue) {
        return (issue.area == null) ? issue.office.name : issue.area.name;
      }

      function getOffice(issue) {
        return issue.projectName;
      }

      function getCreator(issue) {
        if (issue.creatorId == null || issue.creatorId == '') {
          return '';
        }

        var user = vm.model.users[issue.creatorId];
        return user.name + ' ' + user.lastname ;
      }

      function getFullName(issue) {
        if (issue == null) {
          return;
        }
        var user = vm.model.users[issue.userId];
        return (user == null) ? 'No tiene nombre' : user.name + ' ' + user.lastname;
      }

/* ************************************************************************* */
/* ***************************** ORDENACION ******************************** */
/* ************************************************************************* */

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

/* ************************************************************************ */
/* ************************** MENSAJES ************************************ */
/* ************************************************************************ */
      function messageError(error) {
        vm.view.style3 = vm.view.styles3[1];
        vm.view.style4 = vm.view.styles4[2];
        $timeout(function() {
          vm.closeMessage();
        }, 3000);
      }

      function closeMessage() {
        vm.view.style3 = vm.view.styles3[0];
        vm.view.style4 = vm.view.styles4[0];
      }

      function messageLoading() {
        vm.view.style3 = vm.view.styles3[1];
        vm.view.style4 = vm.view.styles4[1];
      }

      function messageSending() {
        vm.view.style3 = vm.view.styles3[1];
        vm.view.style4 = vm.view.styles4[3];
      }

      function messageCreated() {
        vm.view.style3 = vm.view.styles3[1];
        vm.view.style4 = vm.view.styles4[4];
      }

    }
})();

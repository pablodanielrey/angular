(function() {
    'use strict';

    angular
        .module('issues')
        .controller('OrdersCtrl', OrdersCtrl);

    OrdersCtrl.$inject = ['$scope', '$timeout', '$filter', 'Login', 'Issues', 'Users'];

    /* @ngInject */
    function OrdersCtrl($scope, $timeout, $filter,  Login, Issues, Users) {
        var vm = this;

        // variables del modelo
        vm.model = {
          userId: '',
          users: [],
          issues: [],
          selectedIssue: null
        }

        // constantes
        vm.openStatus = 1;
        vm.workingStatus = 2;
        vm.closeStatus = 5;
        vm.pausedStatus = 7;
        vm.rejectedStatus = 6;

        vm.lowPriority = 1;
        vm.normalPriority = 2;
        vm.highPriority = 3;


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
          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'cerrada', 'rechazada', 'pausada'],
          statusSort: ['','abierta', 'enProgreso', 'pausada', 'rechazada', 'cerrada'],
          priorities: ['baja', 'normal', 'alta', 'alta', 'alta'], //solo se maneja el estilo alta, si esta como urgente o inmediata se lo toma solo como alta
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
        vm.selectStatus = selectStatus;
        vm.selectPriotity = selectPriotity;
        vm.cancel = cancel;
        vm.setStatus = setStatus;
        vm.setPriority = setPriority;

        vm.getPriority = getPriority;
        vm.getDate = getDate;
        vm.getDiffDay = getDiffDay;
        vm.getStatus = getStatus;
        vm.getFromOffice = getFromOffice;
        vm.getFromArea = getFromArea;
        vm.getOffice = getOffice;
        vm.getFullName = getFullName;
        vm.getCreator = getCreator;
        vm.registerEventManagers = registerEventManagers;

        vm.sortDate = sortDate;
        vm.sortStatus = sortStatus;
        vm.sortPriority = sortPriority;

        activate();

        function activate() {
          vm.model.userId = Login.getCredentials()['userId']
          vm.initializeView();
          vm.initializeModel();
          vm.registerEventManagers();
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
          vm.model.selectedIssue = null;
          vm.loadIssues();
        }

        // TODO: manejador de eventos
        function registerEventManagers() {
          Issues.subscribe('issues.comment_created_event', function(params) {
            /*var parentId = params[0];
            var commentId = params[1];
            if (vm.model.issueSelected.id == parentId) {
              Issues.findById(commentId).then(
                function(comment) {
                    vm.messageSending();
                    $timeout(function () {
                      vm.view.style2 = vm.view.styles2[0];
                      vm.closeMessage();
                    }, 2500);

                    vm.model.issueSelected.children.push(comment);
                },
                function(error) {
                    vm.messageError(error);
                });
            }*/
          });

          Issues.subscribe('issues.issue_created_event', function(params) {
            /*var issueId = params[0];
            var authorId = params[1];
            var fromOfficeId = params[2];
            var officeId = params[3];
            if (authorId == vm.model.userId || vm.model.userOffices.indexOf(officeId) > -1) {
                Issues.findById(issueId).then(
                  function(issue) {
                    if (issue != null) {
                      vm.model.issues.push(issue);
                    }
                  },
                  function(error) {

                  }
                )
            }*/
          });

        }

/* ************************************************************************ */
/* ******************** CONSULTAS AL MODELO ******************************* */
/* ************************************************************************ */

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
        console.log(issue);
        vm.view.style = vm.view.styles[1];
        vm.model.selectedIssue = issue;
      }

      function selectStatus() {
        vm.view.style2 = (vm.view.style2 == vm.view.styles2[6]) ?  vm.view.styles2[0] : vm.view.styles2[6];
      }

      function selectPriotity() {
        vm.view.style2 = (vm.view.style2 == vm.view.styles2[7]) ?  vm.view.styles2[0] : vm.view.styles2[7];
      }

      function cancel() {
        vm.view.style = vm.view.styles[0];
      }

      function createIssue() {
        vm.view.style = vm.view.styles[3];
      }

      function createComment() {
        vm.view.style = vm.view.styles[2];
      }

      function setStatus(issue, status) {
        vm.view.style2 = vm.view.styles2[0];
        issue.statusId = status;
        Issues.changeStatus(issue, status).then(
          function(data) {

          },
          function(error) {
            $scope.$apply(function() {
              vm.messageError(error);
            })
          }
        )
      }

      function setPriority(issue, priority) {
        vm.view.style2 = vm.view.styles2[0];
        issue.priority = priority;
        Issues.changePriority(issue, priority).then(
          function(data) {

          },
          function(error) {
            $scope.$apply(function() {
              vm.messageError(error);
            })
          }
        )
      }


/* ************************************************************************ */
/* ********************* FORMATO DE DATOS ********************************* */
/* ************************************************************************ */

      function getPriority(issue) {
        if (issue == null) {
          return '';
        }
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
        if (issue == null) {
          return '';
        }
        return (issue.fromOffice == null) ? '' : issue.fromOffice.name;
      }

      function getFromArea(issue) {
        return (issue == null || issue.area == null) ? '' : issue.area.name;
      }

      function getOffice(issue) {
        return issue.projectName;
      }

      function getCreator(issue) {
        if (issue == null || issue.creatorId == null || issue.creatorId == '') {
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
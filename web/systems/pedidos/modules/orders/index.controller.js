(function() {
    'use strict';

    angular
        .module('mainApp')
        .controller('OrdersCtrl', OrdersCtrl);

    OrdersCtrl.$inject = ['$scope', '$timeout', 'Login', 'Issue'];

    /* @ngInject */
    function OrdersCtrl($scope, $timeout, Login, Issue) {
        var vm = this;

        // variables del modelo
        vm.model = {
          userId: '',
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
          styles4: ['', 'mensajeCargando', 'mensajeError', 'mensajeEnviado', 'mensajePedidoCreado']
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

        activate();

        function activate() {
          vm.model.userId = '';
          Login.getSessionData()
            .then(function(s) {
                vm.model.userId = s.user_id;
                vm.initializeModel();
                vm.initializeView();
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
/* **********************  ********************************** */
/* ************************************************************************ */

      function  loadIssues() {
        vm.model.issues = [];
        Issue.getAssignedIssues().then(
          function(issues) {
            
          },
          function(error) {
            $scope.$apply(function() {
              vm.messageError(err);
            })
          }
        );
      }

/* ************************************************************************ */
/* ************************** MENSAJES ************************************ */
/* ************************************************************************ */
      function messageError(error) {
        vm.view.style3 = vm.view.styles3[1];
        vm.view.style4 = vm.view.styles4[2];
        $timeout(function() {
          vm.closeMessage();
        }, 2000);
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

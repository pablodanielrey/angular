(function() {
    'use strict';

    angular
        .module('issues')
        .controller('OrdersDetailCtrl', OrdersDetailCtrl);

    OrdersDetailCtrl.$inject = ['$scope', '$routeParams', '$location', 'Login', 'Issues', 'Users', 'IssuesDD'];

    /* @ngInject */
    function OrdersDetailCtrl($scope, $routeParams, $location, Login, Issues, Users, IssuesDD) {
        var vm = this;

        // variables del modelo
        vm.model = {
          issue: null, //issue inicial
        }

        // variables de la vista
        vm.view = {
          style2: '',
          styles2: ['', 'buscarOficina', 'buscarArea', 'buscarConsulta', 'buscarUsuario', 'buscarOficinaDeUsuario', 'seleccionarEstado', 'seleccionarPrioridad'],
          style3: '',
          styles3: ['','pantallaMensajeAlUsuario'],
          style4: '',
          styles4: ['', 'mensajeCargando', 'mensajeError', 'mensajeEnviado', 'mensajePedidoCreado'],
          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'cerrada', 'rechazada', 'pausada'],
        }

        vm.openStatus = 1;
        vm.workingStatus = 2;
        vm.closeStatus = 5;
        vm.pausedStatus = 7;
        vm.rejectedStatus = 6;

        vm.lowPriority = 1;
        vm.normalPriority = 2;
        vm.highPriority = 3;

        

        // métodos
        vm.issueStatus = issueStatus; //estado del issue
        vm.selectStatus = selectStatus; //seleccion de estado
        vm.setStatus = setStatus; //cambio de estado

        activate();

        function activate() {
          vm.model.userId = Login.getCredentials()['userId'];
          var params = $routeParams;
          IssuesDD.issueDetail(params.issueId).then(
            function(issue){ vm.model.issue = issue; },
            function(error){ console.log(error); }
          )

          vm.view.style2 = vm.view.styles2[0];
          vm.view.style3 = vm.view.styles3[0];
          vm.view.style4 = vm.view.styles4[0];
        };


        function issueStatus() {
          if (vm.model.issue && "statusId" in vm.model.issue) return vm.view.status[vm.model.issue.statusId];
        }

        function selectStatus() {
          vm.view.style2 = (vm.view.style2 == vm.view.styles2[6]) ?  vm.view.styles2[0] : vm.view.styles2[6];
        }

        function setStatus(status) {
          vm.view.style2 = vm.view.styles2[0];
          vm.model.issue.statusId = status;
          Issues.changeStatus(vm.model.issue, status).then(
            function(data) { console.log(data); },
            function(error) { console.log(error); }
          )
        }

    }
})();

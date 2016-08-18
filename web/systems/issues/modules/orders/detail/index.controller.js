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
          priorities: ['', 'baja', 'normal', 'alta', 'alta', 'alta'], //solo se maneja el estilo alta, si esta como urgente o inmediata se lo toma solo como alta
        }


        // métodos
        vm.issueStatus = issueStatus; //estado del issue
        vm.selectStatus = selectStatus; //seleccion de estado
        vm.setStatus = setStatus; //cambio de estado

        vm.issuePriority = issuePriority; //estado del issue
        vm.selectPriority = selectPriority; //seleccion de estado
        vm.setPriority = setPriority; //cambio de estado

        activate();

        function activate() {
          vm.model.userId = Login.getCredentials()['userId'];
          var params = $routeParams;
          IssuesDD.issueDetail(params.issueId).then(
            function(issue){ vm.model.issue = issue; console.log(vm.model.issue)},
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
          var statusId = vm.view.status.indexOf(status);
          vm.model.issue.statusId = statusId;

          Issues.changeStatus(vm.model.issue, statusId).then(
            function(data) { console.log(data); },
            function(error) { console.log(error); }
          )
        }

        function issuePriority() {
          if (vm.model.issue && "priority" in vm.model.issue) return vm.view.priorities[vm.model.issue.priority];
        }


        function selectPriority() {
          vm.view.style2 = (vm.view.style2 == vm.view.styles2[7]) ?  vm.view.styles2[0] : vm.view.styles2[7];
        }

        function setPriority(priority) {
          vm.view.style2 = vm.view.styles2[0];
          var priorityId = vm.view.priorities.indexOf(priority);
          vm.model.issue.priority = priorityId;

          Issues.changePriority(vm.model.issue, priorityId).then(
            function(data) { console.log(data); },
            function(error) { console.log(error); }
          )
        }


    }
})();

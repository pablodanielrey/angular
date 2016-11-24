(function() {
    'use strict';

    angular
        .module('assistance')
        .controller('HistoryCtrl', HistoryCtrl);

    HistoryCtrl.$inject = ['$scope', 'Login'];

    /* @ngInject */
    function HistoryCtrl($scope, Login) {
        var vm = this;

        vm.model = {
          history: []
        }

        vm.view = {
          activate: false,
          styleHistory: {'Cambio de horario semanal' : 'historialHorarioSemanal' ,'Cambio de horario semanal por horas': 'historialHorarioSemanalSerenos', 'Horario especial': 'historialHorarioEspecial '}
        }

        vm.viewDetail = viewDetail;
        vm.getStyleHistory = getStyleHistory;
        vm.remove = remove;

        $scope.$on('wamp.open', function(event, args) {
          activate();
        });

        activate();

        function activate() {
          if (vm.view.activate || Login.getPrivateTransport() == null) {
            return;
          }
          vm.view.activate = true;
          loadHistory();
        }

        /*
          EVENTOS
        */
        function registerEventManagers() {
          Assistance.subscribe('assistance.remove_schedules_event', function(params) {
            var historyId = params[0];
            _deleteArray(historyId);
          });

          Assistance.subscribe('assistance.add_schedules_event', function(params) {
            var historyId = params[0];
            Assistance.findHistoryById([historyId]).then(function(history) {
              vm.model.history.push(history);
            })
          });
        }
        /*
          VISUAL
        */
        function _deleteArray(id) {
          for (var i = 0; i < vm.model.history.length; i++) {
            if (vm.model.history[i].id == id) {
              vm.model.history.splice(i, 1);
              return;
            }
          }
        }

        function viewDetail(item) {
          item.displayDetail = !item.displayDetail;
        }

        function getStyleHistory(item) {
          return vm.view.styleHistory[item.description];
        }

        /*
          LLAMADAS AL SERVIDOR
        */

        function loadHistory() {
          vm.model.history = [];
          vm.model.history.push({id: 1, created: new Date(), description: 'Horario especial', schedules: [], displayDetail: false});
          vm.model.history.push({id: 2, created: new Date(), description: 'Cambio de horario semanal', schedules: [], displayDetail: false});
        }

        function remove(item) {
          _deleteArray(item.id);
        }


    }
})();

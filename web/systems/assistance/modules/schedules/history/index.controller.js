(function() {
    'use strict';

    angular
        .module('assistance')
        .controller('HistoryCtrl', HistoryCtrl);

    HistoryCtrl.$inject = ['$scope', 'Login', 'Assistance', '$routeParams', '$timeout'];

    /* @ngInject */
    function HistoryCtrl($scope, Login, Assistance, $routeParams, $timeout) {
        var vm = this;

        vm.model = {
          history: [],
          selectedPerson: null
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

          var params = $routeParams;
          if ('personId' in params) {
            vm.model.selectedPerson = params.personId;
          } else {
            vm.model.selectedPerson =  Login.getCredentials()['userId'];
          }

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

        function _parseHistory(elem) {
          elem.displayDetail = false;
          return elem;
        }

        /*
          LLAMADAS AL SERVIDOR
        */

        function loadHistory() {
          vm.model.history = [];
          Assistance.findAllSchedules(vm.model.selectedPerson).then(Assistance.findSchedHistoryByIds).then(function(history) {
            for (var i = 0; i < history.length; i++) {
              vm.model.history.push(_parseHistory(history[i]));
            }
          }, function(error) {
            console.log(error);
          });
          /*
          var start = new Date(); start.setHours(8); start.setMinutes(0);
          var end = new Date(); end.setHours(15); end.setMinutes(0);
          vm.model.history.push({id: 1, created: new Date(), date: new Date(), description: 'Horario especial', schedules: [{date: new Date(), start: start, end:end}], displayDetail: false});
          vm.model.history.push({id: 2, created: new Date(), date: new Date(), description: 'Cambio de horario semanal', schedules: [{date: new Date(), start: start, end:end}], displayDetail: false});
          */
        }

        function remove(item) {
          Assistance.removeScheduleHistory(item).then(function(id) {
            $timeout(function () {
              _deleteArray(item.id);
            });
          }, function(error) {
            console.error(error);
          })

        }


    }
})();

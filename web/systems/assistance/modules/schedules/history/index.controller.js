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
          selectedPerson: null,

          selected: null
        }

        vm.view = {
          activate: false,
          styleHistory: {'Cambio de horario semanal' : 'historialHorarioSemanal' ,'Cambio de horario semanal por horas': 'historialHorarioSemanalSerenos', 'Horario especial': 'historialHorarioEspecial '}
        }

        vm.viewDetail = viewDetail;
        vm.getStyleHistory = getStyleHistory;
        vm.deleteItem = deleteItem;

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
          registerEventManagers();
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
          if (item.displayDetail && item.schedulesObj == null) {
            Assistance.findScheduleByIds(item.schedules).then(function(schedules) {
              var schedulesObj = [];
              for (var i = 0; i < schedules.length; i++) {
                if (schedules[i].isNull) {
                  continue;
                }
                schedulesObj.push( _parseSchedule(schedules[i]));
              }
              $timeout(function () {
                item.schedulesObj = schedulesObj;
              });
            }, function(error) {
              console.error(error);
            })
          }
        }

        function deleteItem(item) {
          vm.model.selected = item;
          $scope.$parent.vm.displayMessageDelete(item);
        }

        // daily,date,end,id,isNull,special,start,userId,weekday
        function _parseSchedule(sc) {
          // getDay() => [Sunday, Monday, ..., Saturday]
          var sortDay = [6, 0, 1, 2, 3, 4, 5];
          var date = new Date(sc.date);
          var weekday = sortDay[date.getDay()];

          var diff = (sc.weekday - weekday) * 24 * 3600 * 1000;


          var millisStart = (sc.start == null) ? null : sc.start * 1000;
          var start = (millisStart == null) ? null : new Date(date.getTime() + millisStart + diff);

          var millisEnd =  (sc.end == null) ? null : sc.end * 1000;
          var end = (millisEnd == null) ? null : new Date(date.getTime() + millisEnd + diff);

          var limitMillis = 24 * 60 * 60 * 1000;
          if (start != null && end != null && (end.getTime() - start.getTime()) > limitMillis) {
            start = null;
            end = null;
          }

          var hours = Math.trunc((end - start) / 1000 / 60 / 60);

          return {date: date, weekday:sc.weekday, start: start, end: end, hours: hours}
        }

        function getStyleHistory(item) {
          return vm.view.styleHistory[item.description];
        }

        function _parseHistory(elem) {
          elem.displayDetail = false;
          elem.schedulesObj = null;
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
            console.log(vm.model.history);
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



    }
})();

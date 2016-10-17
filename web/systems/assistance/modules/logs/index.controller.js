(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('LogsCtrl', LogsCtrl);

    LogsCtrl.$inject = ['$scope', 'Assistance', 'Users', 'Login', 'Files', '$timeout', '$window', '$filter'];

    function _getDateInTime(hours, minutes, seconds) {
      var d = new Date()
      d.setHours(hours);
      d.setMinutes(minutes);
      d.setSeconds(seconds);
      d.setMilliseconds(0);
      return d;
    }

    function LogsCtrl($scope, Assistance, Users, Login, Files, $timeout, $window, $filter) {
        var vm = this;

        vm.view = {
          style2: '',
          style: '',
          searchInput: '',
          sort: '',
          reverse: true
        }

        vm.model = {
          search: {
            initDate: new Date(),
            endDate: new Date(),
            initHour: _getDateInTime(0,0,0),
            endHour: _getDateInTime(23,59)
          },
          logs: [],
          todayLogs: [],
          status: [],
          statusToday: [],
          inside: 0,
          outside: 0,
          activate: false //para saber si ya se ejecuto el activate. Solucion a que el wamp open se ejecuta tres veces el wamp.open
        };

        vm.resetSearchAndGetLogs = resetSearchAndGetLogs;
        vm.searchLogs = searchLogs;
        vm.sortDate = sortDate;
        vm.sortAccess = sortAccess;
        vm.sortName = sortName;
        vm.sortHours = sortHours;
        vm.sortDni = sortDni;
        vm.sortType = sortType;
        vm.download = download;

        $scope.$on('wamp.open', function(event, args) {
          activate();
        });

        activate();

        function activate() {
          if (vm.model.activate || Login.getPrivateTransport() == null) {
            return;
          }
          vm.model.activate = true;
          _getTodayLogs();
          resetSearchAndGetLogs();
        }


        /* ********************************************************************************
                              MÉTODOS DE ORDENACIÓN
         * ******************************************************************************** */
       /*
         Dispara la ordenación del listado.
       */
       function sortIssues() {
         var order = $window.sessionStorage.getItem('listSortLogs');
         if (order == null) {
           order = ['-date'];
           $window.sessionStorage.setItem('listSortLogs', JSON.stringify(order));
         } else {
           order = JSON.parse(order);
         }
         vm.model.logs = $filter('orderBy')(vm.model.logs, order, false);
       }

       /*
         retorna el valor de orden inverso o order normal. y almacena el inverso.
         solo se usa cuando se clickea el ordenamiento explícitamente.
         no cuando se ordena el listado.
       */
       function _processSortRev() {
         var rev = $window.sessionStorage.getItem('reverseSortLogs');
         if (rev == null) {
           rev = false;
           $window.sessionStorage.setItem('reverseSortLogs', JSON.stringify(!rev));
         } else {
           rev = JSON.parse(rev);
         }

         // almaceno el orden a inverso.
         if (rev) {
           $window.sessionStorage.setItem('reverseSortLogs', JSON.stringify(!rev));
         } else {
           $window.sessionStorage.setItem('reverseSortLogs', JSON.stringify(!rev));
         }

         return rev;
       }

        function sortDate() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ['-date'];
          } else {
            order = ['date'];
          }
          $window.sessionStorage.setItem('listSortLogs', JSON.stringify(order));
          sortIssues();
        }

        function sortHours() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["date.getHours()","date.getMinutes()", "date.getSeconds()"];
          } else {
            order = ["-date.getHours()","-date.getMinutes()", "-date.getSeconds()"];
          }
          $window.sessionStorage.setItem('listSortLogs', JSON.stringify(order));
          sortIssues();
        }

        function sortName() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["name", "lastname", "date"];
          } else {
            order = ["-name", "-lastname", "date"];
          }
          $window.sessionStorage.setItem('listSortLogs', JSON.stringify(order));
          sortIssues();
        }

        function sortAccess() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["clase", "date", "name", "lastname"];
          } else {
            order = ["-clase", "date", "name", "lastname"];
          }
          $window.sessionStorage.setItem('listSortLogs', JSON.stringify(order));
          sortIssues();
        }

        function sortDni() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["dni", "date"];
          } else {
            order = ["-dni", "date"];
          }
          $window.sessionStorage.setItem('listSortLogs', JSON.stringify(order));
          sortIssues();
        }

        function sortType() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["tipo", "date"];
          } else {
            order = ["-tipo", "date"];
          }
          $window.sessionStorage.setItem('listSortLogs', JSON.stringify(order));
          sortIssues();
        }


        /* ---------------------------------------------------------------------------- */


        function _resetSearch() {
          vm.model.search = {
            initDate: new Date(),
            endDate: new Date(),
            initHour: _getDateInTime(0,0,0),
            endHour: _getDateInTime(23,59,0)
          }
        }


        function searchLogs() {
          vm.view.style2 = '';
          _getLogs();
        }

        function resetSearchAndGetLogs() {
          vm.view.style2 = '';
          _resetSearch();
          _getLogs();
        }

        /* ********************************************************************************
                        Estado de los ususarios (si se encuentra afuera o adentro)
         * ******************************************************************************** */

        function _getStatus(userId) {
          for (var i = 0; i < vm.model.status.length; i++) {
            if (vm.model.status[i].id == userId) {
              return vm.model.status[i].status;
            }
          }
          return false;
        }

        function _calcStatus(userId) {
          for (var i = 0; i < vm.model.status.length; i++) {
            if (vm.model.status[i].id == userId) {
              vm.model.status[i].status = !(vm.model.status[i].status);
              if (vm.model.status[i].status) {
                vm.model.inside = vm.model.inside + 1;
                return true;
              } else {
                vm.model.inside = (vm.model.inside == 0) ? 0 : vm.model.inside - 1;
                vm.model.outside = vm.model.outside + 1;
                return false;
              }
            }
          }
          vm.model.inside = vm.model.inside + 1;
          vm.model.status.push({id:userId, status:true});
          return true;
        }

        function _calcStatusToday(userId) {
          for (var i = 0; i < vm.model.statusToday.length; i++) {
            if (vm.model.statusToday[i].id == userId) {
              vm.model.statusToday[i].status = !(vm.model.statusToday[i].status);
              if (vm.model.statusToday[i].status) {
                return true;
              } else {
                return false;
              }
            }
          }
          vm.model.statusToday.push({id:userId, status:true});
          return true;
        }

        function _resetStatus() {
          vm.model.status = [];
          vm.model.inside = 0;
          vm.model.outside = 0;
        }

        // ------------------------------------------------------------------------------------

        /* ********************************************************************************
                                Obtenención de los logs
         * ******************************************************************************** */


        // parsea los logs a mostrar
        function _parseLog(log, cca) {
          var d = new Date(log.log);
          var photo = (log.user != null && log.user.photoSrc != '') ? log.user.photoSrc : "/systems/issues/img/avatarMan.jpg";
          return {
              clase: cca,
              tipo: 'NoDocente',
              name: log.user.name.trim(),
              lastname: log.user.lastname.trim(),
              photoSrc: photo,
              dni: log.user.dni,
              date: d
          }
        }


        function _parseToday(log) {
          var cca = _calcStatusToday(log.user.id) ? 'entrada' : 'salida';
          return _parseLog(log, cca);
        }

        function _parseAll(log) {
          var cca = _calcStatus(log.user.id) ? 'entrada' : 'salida';
          return _parseLog(log, cca);
        }


        // obtiene un resumen de los últimos logs
        function _getTodayLogs() {
          vm.model.todayLogs = [];
          var dayMillis = 24 * 60 * 60 * 1000;
          var start = new Date();
          start.setHours(0); start.setMinutes(0); start.setSeconds(0);
          var end = new Date(start.getTime() + (dayMillis) - 1000);
          Assistance.getLogs(start, end, start, end).then(Assistance.findUsersByLogs).then(Assistance.findUserPhotos).then(Assistance.photoToDataUri).then(
            function(logs) {
              $timeout(function () {
                for (var i = 0; i < logs.length; i++) {
                  vm.model.todayLogs.push(_parseToday(logs[i]));
                }
              });
            }, function(error) {
              console.log(error);
            }
          );
        }

        // obtiene los logs
        function _getLogs() {
          vm.model.logs = [];
          _resetStatus();

          var s = vm.model.search;
          vm.view.style = 'cargando';
          var sHour = (s.initHour == null) ? _getDateInTime(0,0,0) : s.initHour;
          var eHour = (s.endHour == null) ? _getDateInTime(23,59,59) : s.endHour;
          Assistance.getLogs(s.initDate, s.endDate, sHour, eHour).then(Assistance.findUsersByLogs).then(function(logs){
            $timeout(function () {
              for (var i = 0; i < logs.length; i++) {
                vm.model.logs.push(_parseAll(logs[i]));
              }
              vm.view.style = '';
              sortIssues();
            });
          }, function(err) {
            console.log(err);
          })
        }

        // obtiene los logs
        function download() {
          var s = vm.model.search;
          var sHour = (s.initHour == null) ? _getDateInTime(0,0,0) : s.initHour;
          var eHour = (s.endHour == null) ? _getDateInTime(23,59,59) : s.endHour;
          Assistance.exportLogs(s.initDate, s.endDate, sHour, eHour).then(function(file) {
            console.log(file);
          }, function(err) {
            console.log(err);
          })
        }


    };



})();

(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('ReportsCtrl', ReportsCtrl);

    ReportsCtrl.$inject = ['$scope', 'Assistance', 'Users', '$timeout', 'Login', '$window', 'Offices', '$filter'];

    function ReportsCtrl($scope, Assistance, Users, $timeout, Login, $window, Offices, $filter) {
        var vm = this;

        vm.model = {
          users: {},
          statistics: [],

          search: {
            start: new Date(),
            end: new Date(),
            offices: [],
            text: '',
            sTime: new Date(),
            eTime: new Date()
          },
          header: {
            columns:[],
            offices: [],
            officeIds: []
          },
          activate: false //para saber si ya se ejecuto el activate. Solucion a que el wamp open se ejecuta tres veces el wamp.open
        }

        vm.view = {
          style: ''
        }

        vm.findStatistics = findStatistics;
        vm.print = print;
        vm.download = download;

        // metodos visuales
        vm.getOffices = getOffices;
        vm.resetFilters = resetFilters;

        vm.getInMode = getInMode;
        vm.getOutMode = getOutMode;

        vm.getWorkedHours = getWorkedHours;

        vm.setNote = setNote;

        $scope.$on('wamp.open', function(event, args) {
          activate();
        });

        activate();



        function activate() {
          if (vm.model.activate || Login.getPrivateTransport() == null) {
            return;
          }
          vm.model.activate = true;
          _loadOffices();
        }



// ************************************************************************
//                    FILTROS
// ************************************************************************

        function _initializeFilters() {
          vm.model.search = {
            start: new Date(),
            end: new Date(),
            offices: vm.model.header.officeIds,
            text: '',
            sTime: new Date(),
            eTime: new Date()
          }
          _initTime(vm.model.search.sTime, 0, 0, 0);
          _initTime(vm.model.search.eTime, 23, 59, 0);

          vm.model.header.columns = [];
        }

        function _initTime(date, hours, minutes, seconds) {
          date.setHours(hours);
          date.setMinutes(minutes);
          date.setSeconds(seconds);
          date.setMilliseconds(0);
        }

        function _loadOffices() {
          vm.model.header.offices = [];
          Offices.findAll().then(Offices.findById).then(
            function(off) {
              vm.model.header.officeIds = [];
              vm.model.header.offices = off;
              for (var i = 0; i < off.length; i++) {
                vm.model.header.officeIds.push(off[i].id);
              }
              resetFilters();
            });
        }

        function resetFilters() {
          _initializeFilters();
          vm.findStatistics();
        }

        function getOffices() {
          return vm.model.header.offices;
        }

        function print() {
          $window.print();
        }

        function download() {
          var initDate = angular.copy(vm.model.search.start);
          var endDate = angular.copy(vm.model.search.end);
          var initTime = vm.model.search.sTime;
          var endTime = vm.model.search.eTime;
          _initTime(initDate, 0, 0, 0);
          _initTime(endDate, 23, 59, 59);

          Assistance.exportStatistics(initDate, endDate, [], vm.model.search.offices, initTime, endTime).then(function(stats) {
            console.log(stats);
          }, function(err) {
            console.log(err);
          });
        }

        /* ********************************************************************************
                              MÉTODOS DE ORDENACIÓN
         * ******************************************************************************** */
       /*
         Dispara la ordenación del listado.
       */
       function sortReports() {
         var order = $window.sessionStorage.getItem('listSortReports');
         if (order == null) {
           order = ['user.name', 'user.lastname', 'user.date'];
           $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
         } else {
           order = JSON.parse(order);
         }
         if (order[0] == 'user.dni' || order[0] == '-user.dni') {
           vm.model.statistics = $filter('orderBy')(vm.model.statistics, order, false, dniComparator);
         } else {
           vm.model.statistics = $filter('orderBy')(vm.model.statistics, order, false, localeSensitiveComparator);
         }
       }

       /*
         retorna el valor de orden inverso o order normal. y almacena el inverso.
         solo se usa cuando se clickea el ordenamiento explícitamente.
         no cuando se ordena el listado.
       */
       function _processSortRev() {
         var rev = $window.sessionStorage.getItem('reverseSortReports');
         if (rev == null) {
           rev = false;
           $window.sessionStorage.setItem('reverseSortReports', JSON.stringify(!rev));
         } else {
           rev = JSON.parse(rev);
         }

         // almaceno el orden a inverso.
         if (rev) {
           $window.sessionStorage.setItem('reverseSortReports', JSON.stringify(!rev));
         } else {
           $window.sessionStorage.setItem('reverseSortReports', JSON.stringify(!rev));
         }

         return rev;
       }

       function localeSensitiveComparator(v1, v2) {
         // If we don't get strings, just compare by index
         if (v1.type !== 'string' || v2.type !== 'string') {
           return (v1.index < v2.index) ? -1 : 1;
         }

         // Compare strings alphabetically, taking locale into account
         return v1.value.localeCompare(v2.value);
       };

       function dniComparator(v1, v2) {
         // If we don't get strings, just compare by index
         if (v1.type !== 'string' || v2.type !== 'string') {
           return (v1.index < v2.index) ? -1 : 1;
         }

         // Compare strings alphabetically, taking locale into account
         if (v1.value.length == v2.value.length) {
           return v1.value.localeCompare(v2.value);
         }
         return (v1.value.length < v2.value.length) ? -1 : 1;
       };

       vm.sortName = sortName;
       vm.sortDni = sortDni;
       vm.sortPosition = sortPosition;

        function sortName() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ['user.name', 'user.lastname', 'user.date'];
          } else {
            order = ['-user.name', '-user.lastname', 'user.date'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          sortReports();
        }

        function sortDni() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ['user.dni', 'user.date'];
          } else {
            order = ['-user.dni', 'user.date'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          sortReports();
        }

        function sortPosition() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ['position','user.name', 'user.lastname', 'user.date'];
          } else {
            order = ['-position','user.name', 'user.lastname', 'user.date'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          sortReports();
        }

// ***********************************************************************


        function getWorkedHours(seconds) {
          var minutes = ('0' + Math.floor(seconds / 60 % 60)).substr(-2, 2);
          return Math.floor(seconds / 60 / 60) + ':' + minutes;
        }


        function getInMode(i) {
          if (i.startMode == null || i.startMode == 'UNDEFINED') {
            return '';
          }

          return (i.startMode == 1) ? 'entradaPorHuella' : 'entradaPorTeclado';
        }

        function getOutMode(i) {
          if (i.endMode == null || i.endMode == 'UNDEFINED') {
            return '';
          }

          return (i.endMode == 1) ? 'salidaPorHuella' : 'salidaPorTeclado';
        }


/* **************************************************************************
                PARSEO DE ESTADISTICAS
 * ************************************************************************** */

        function _parseStatic(stat) {
          var justification = (stat.justification != null && stat.justification.status == 2) ? stat.justification : null;
          return {
            date: (stat.date != null) ? new Date(stat.date) : null,
            iin: (stat.logStart != null) ? new Date(stat.logStart) : null,
            startMode: stat.startMode,
            endMode: stat.endMode,
            out: (stat.logEnd != null) ? new Date(stat.logEnd) : null,
            start: (stat.scheduleStart != null) ? new Date(stat.scheduleStart) : null,
            end: (stat.scheduleEnd != null) ? new Date(stat.scheduleEnd) : null,
            user: stat.user,
            position: stat.position,
            userId: stat.userId,
            workedSeconds: stat.workedSeconds,
            justification: justification,
            notes: stat.notes
          }
        }

/* **************************************************************************
                BUSQUEDAS DE ESTADISTICAS
 * ************************************************************************** */

        function findStatistics() {
          var initDate = angular.copy(vm.model.search.start);
          var endDate = angular.copy(vm.model.search.end);
          var initTime = vm.model.search.sTime;
          var endTime = vm.model.search.eTime;
          vm.model.statistics = [];
          _initTime(initDate, 0, 0, 0);
          _initTime(endDate, 23, 59, 59);

          Assistance.getStatistics(initDate, endDate, [], vm.model.search.offices, initTime, endTime).then(Assistance.findUsersByStatics).then(function(stats) {
            $timeout(function() {
              var uids = [];
              for (var i = 0; i < stats.length; i++) {
                uids.push(stats[i].userId);
                vm.model.statistics.push(_parseStatic(stats[i]));
              }
              sortReports();
            });
          }, function(err) {
            console.log(err);
          });
        }

    /* **************************************************************************
                                    NOTAS
     * ************************************************************************** */

     function setNote(stat) {
       Assistance.setWorkedNote(stat.userId, stat.date, stat.notes).then(function(data) {
         console.log("Ok");
       }, function(error) {
         console.error(error);
         $timeout(function () {
           stat.notes = '';
         }, 0);
       })
     }

  }

})();

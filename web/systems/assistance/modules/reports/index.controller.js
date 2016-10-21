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

        vm.sortName = sortName;
        vm.sortDni = sortDni;
        vm.sortPosition = sortPosition;
        vm.sortDayStartSchedule = sortDayStartSchedule;
        vm.sortDateStartSchedule = sortDateStartSchedule;
        vm.sortStartSchedule = sortStartSchedule;
        vm.sortDayEndSchedule = sortDayEndSchedule;
        vm.sortDateEndSchedule = sortDateEndSchedule;
        vm.sortEndSchedule = sortEndSchedule;
        vm.sortSchedule = sortSchedule;
        vm.sortDayStart = sortDayStart;
        vm.sortDateStart = sortDateStart;
        vm.sortStart = sortStart;
        vm.sortDayEnd = sortDayEnd;
        vm.sortDateEnd = sortDateEnd;
        vm.sortEnd = sortEnd;
        vm.sortHours = sortHours;
        vm.sortJustifications = sortJustifications;
        vm.sortNotes = sortNotes;

        vm.getWorkedHours = getWorkedHours;
        vm.isHidden = isHidden;
        vm.updateColumns = updateColumns;
        vm.updateFilters = updateFilters;

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
          _initColumns();
          _loadOffices();
        }



// ************************************************************************
//                    FILTROS
// ************************************************************************
        function defaultFilters() {
          var search = {
            start: new Date(),
            end: new Date(),
            offices: vm.model.header.officeIds,
            text: '',
            sTime: new Date(),
            eTime: new Date()
          }
          _initTime(search.sTime, 0, 0, 0);
          _initTime(search.eTime, 23, 59, 0);
          return search;
        }


        function _initializeFilters() {
          var filters = $window.sessionStorage.getItem('filtersReports');
          if (filters == null) {
            filters = defaultFilters();
            $window.sessionStorage.setItem('filtersReports', JSON.stringify(filters));
          } else {
            filters = JSON.parse(filters);
            filters.start = new Date(filters.start);
            filters.end = new Date(filters.end);
            filters.sTime = new Date(filters.sTime);
            filters.eTime = new Date(filters.eTime);
          }
          vm.model.search = filters;
        }

        function updateFilters() {
          $window.sessionStorage.setItem('filtersReports', JSON.stringify(vm.model.search));
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
              _init();
            });
        }

        function _init() {
          _initColumns();
          _initializeFilters();
          vm.findStatistics();
        }

        function resetFilters() {
          $window.sessionStorage.removeItem('filtersReports');
          $window.sessionStorage.removeItem('columnsReports');
          $window.sessionStorage.removeItem('listSortReports');
          $window.sessionStorage.removeItem('reverseSortReports');
          _initColumns();
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

          Assistance.exportStatistics(initDate, endDate, [], vm.model.search.offices, initTime, endTime).then(function(file) {
            if (file != null && file != '') {
              console.log(file);
              var url = "https://docs.google.com/spreadsheets/d/" + file;
              $window.open(url, "_blank");
            } else {
              alert('error de generación');
            }
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
           $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
         } else {
           order = JSON.parse(order);
         }

         var comparator = $window.sessionStorage.getItem('comparator');
         if (comparator == null) {
           comparator = "localeSensitiveComparator";
           $window.sessionStorage.setItem('comparator', comparator);
         }

         vm.model.statistics = $filter('orderBy')(vm.model.statistics, order, false, eval(comparator));

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

       /*
        En caso de que sea string utiliza el localeCompare, para que ordene correctamente los acentos
       */
       function localeSensitiveComparator(v1, v2) {
         if (v1.type === 'number' && v2.type === 'number') {
           return (v1.value < v2.value) ? -1 : (v1.value == v2.value) ? 0 : 1;
         }

         if (v1.value == undefined || v2.value == undefined) {
           return (v1.value == undefined) ? -1 : 1;
         }

         if (v1.type !== 'string' || v2.type !== 'string') {
           return (v1.value < v2.value) ? -1 : (v1.value == v2.value) ? 0 : 1;
         }

         // Compare strings alphabetically, taking locale into account
         return v1.value.localeCompare(v2.value);
       };

       /*
        Esta comparacion tiene en cuenta la longitud del string
       */
       function dniComparator(v1, v2) {
         // If we don't get strings, just compare by index
         if (v1.type !== 'string' || v2.type !== 'string') {
           return (v1.index < v2.index) ? -1 : (v1.index == v2.index) ? 0 : 1;
         }

         return (v1.value.length == v2.value.length) ? v1.value.localeCompare(v2.value) : (v1.value.length < v2.value.length) ? -1 : 1;
       };

       function dayComparator(v1, v2) {
         if (v1.type === 'object' && !isNaN(v1.value) && v2.type === 'object' && !isNaN(v2.value)) {
           var d1 = new Date(v1.value).getDay();
           var d2 = new Date(v2.value).getDay();
           return (d1 < d2) ? -1 : (d1 == d2) ? 0 : 1;
         }

         if (v1.value == "null" || v2.value == 'null') {
           return (v1.value == "null") ? -1 : 1;
         }

         return localeSensitiveComparator(v1, v2)
       };


        function sortName() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ['user.name', 'user.lastname', 'date'];
          } else {
            order = ['-user.name', '-user.lastname', 'date'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortDni() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ['user.dni', 'date'];
          } else {
            order = ['-user.dni', 'date'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "dniComparator");
          sortReports();
        }

        function sortPosition() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ['position','user.name', 'user.lastname', 'date'];
          } else {
            order = ['-position','user.name', 'user.lastname', 'date'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortDayStartSchedule() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["date", 'user.name', 'user.lastname', 'date'];
          } else {
            order = ["-date", 'user.name', 'user.lastname', 'date'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "dayComparator");
          sortReports();
        }

        function sortDateStartSchedule() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["date | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          } else {
            order = ["-date | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortStartSchedule() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["start | date: 'HH:mm'", "end | date: 'HH:mm'", "start | date: 'dd/MM/yyyy'",'user.name', 'user.lastname'];
          } else {
            order = ["-start | date: 'HH:mm'", "end | date: 'HH:mm'", "start | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortDayEndSchedule() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["end", 'user.name', 'user.lastname', 'end'];
          } else {
            order = ["-end", 'user.name', 'user.lastname', 'end'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "dayComparator");
          sortReports();
        }

        function sortDateEndSchedule() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["end | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          } else {
            order = ["-end | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortEndSchedule() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["end | date: 'HH:mm'", "end | date: 'dd/MM/yyyy'",'user.name', 'user.lastname'];
          } else {
            order = ["-end | date: 'HH:mm'", "end | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortSchedule() {
          sortStartSchedule();
        }

        function sortDayStart() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["iin", 'user.name', 'user.lastname', 'iin'];
          } else {
            order = ["-iin", 'user.name', 'user.lastname', 'iin'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "dayComparator");
          sortReports();
        }

        function sortDateStart() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["iin | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          } else {
            order = ["-iin | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortStart() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["iin | date: 'HH:mm'", "iin | date: 'dd/MM/yyyy'",'user.name', 'user.lastname'];
          } else {
            order = ["-iin | date: 'HH:mm'", "iin | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortDayEnd() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["out", 'user.name', 'user.lastname', 'out'];
          } else {
            order = ["-out", 'user.name', 'user.lastname', 'out'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "dayComparator");
          sortReports();
        }

        function sortDateEnd() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["out | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          } else {
            order = ["-out | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortEnd() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["out | date: 'HH:mm'", "out | date: 'dd/MM/yyyy'",'user.name', 'user.lastname'];
          } else {
            order = ["-out | date: 'HH:mm'", "out | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortHours() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["workedSeconds",'user.name', 'user.lastname'];
          } else {
            order = ["-workedSeconds", 'user.name', 'user.lastname'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortJustifications() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["justification.identifier",'user.name', 'user.lastname', 'date'];
          } else {
            order = ["-justification.identifier", 'user.name', 'user.lastname', 'date'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

        function sortNotes() {
          var order = null;
          var rev = _processSortRev();
          if (rev) {
            order = ["notes",'user.name', 'user.lastname', 'date'];
          } else {
            order = ["-notes", 'user.name', 'user.lastname', 'date'];
          }
          $window.sessionStorage.setItem('listSortReports', JSON.stringify(order));
          $window.sessionStorage.setItem('comparator', "localeSensitiveComparator");
          sortReports();
        }

/* **************************************************************************
                        MANEJO DE LAS COLUMNAS
 * ************************************************************************** */

        function updateColumns() {
          $window.sessionStorage.setItem('columnsReports', JSON.stringify(vm.model.header.columns));
        }

        function isHidden(value) {
          for (var i = 0; i < vm.model.header.columns.length; i++) {
            var e = vm.model.header.columns[i];
            if (e.value == value) {
              return !e.visible;
            }
          }
        }

        function _initColumns() {
          var columns = $window.sessionStorage.getItem('columnsReports');
          if (columns == null) {
            columns = defaultColumns();
            $window.sessionStorage.setItem('columnsReports', JSON.stringify(columns));
          } else {
            columns = JSON.parse(columns);
          }
          vm.model.header.columns = columns;
        }

        function defaultColumns() {
           return [
              {value:'name', visible: true, display: 'Nombre y Apellido'},
              {value:'dni', visible: true, display: 'DNI'},
              {value:'position', visible: true, display: 'Cargo'},
              {value:'dayStartSchedule', visible: true, display: 'Día horario ent.'},
              {value:'dateStartSchedule', visible: true, display: 'Fecha horario ent.'},
              {value:'startSchedule', visible: false, display: 'Horario de ent.'},
              {value:'dayEndSchedule', visible: false, display: 'Día horario sal.'},
              {value:'dateEndSchedule', visible: false, display: 'Fecha horario sal.'},
              {value:'endSchedule', visible: false, display: 'Horario de sal.'},
              {value:'shortSchedule', visible: true, display: 'Horario'},
              {value:'dayStart', visible: false, display: 'Día de entrada'},
              {value:'dateStart', visible: false, display: 'Fecha de entrada'},
              {value:'start', visible: true, display: 'Hora de entrada'},
              {value:'dayEnd', visible: false, display: 'Día de salida'},
              {value:'dateEnd', visible: false, display: 'Fecha de salida'},
              {value:'end', visible: true, display: 'Hora de salida'},
              {value:'hours', visible: true, display: 'Horas trabajadas'},
              {value:'justifications', visible: true, display: 'Justificaciones'},
              {value:'notes', visible: true, display: 'Notas'}
            ];
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
          vm.updateFilters();
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

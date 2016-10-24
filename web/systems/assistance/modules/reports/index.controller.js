(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('ReportsCtrl', ReportsCtrl);

    ReportsCtrl.$inject = ['$scope', 'Assistance', 'Users', '$timeout', 'Login', '$window', 'Offices', '$filter', 'AssistanceUtils'];

    function ReportsCtrl($scope, Assistance, Users, $timeout, Login, $window, Offices, $filter, AssistanceUtils) {
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
          AssistanceUtils.clearSort('listSortReports');
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

        function sortName() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ['user.name', 'user.lastname', 'date'] : ['-user.name', '-user.lastname', 'date'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortDni() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ['user.dni', 'date'] : ['-user.dni', 'date'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "dniComparator");
        }

        function sortPosition() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ['position','user.name', 'user.lastname', 'date'] : ['-position','user.name', 'user.lastname', 'date'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortDayStartSchedule() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["date", 'user.name', 'user.lastname', 'date'] : ["-date", 'user.name', 'user.lastname', 'date'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "dayComparator");
        }

        function sortDateStartSchedule() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["date | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'] : ["-date | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortStartSchedule() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["start | date: 'HH:mm'", "end | date: 'HH:mm'", "start | date: 'dd/MM/yyyy'",'user.name', 'user.lastname'] : ["-start | date: 'HH:mm'", "end | date: 'HH:mm'", "start | date: 'dd/MM/yyyy'",'user.name', 'user.lastname'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortDayEndSchedule() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["end", 'user.name', 'user.lastname', 'end'] : ["-end", 'user.name', 'user.lastname', 'end'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "dayComparator");
        }

        function sortDateEndSchedule() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["end | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'] : ["-end | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortEndSchedule() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["end | date: 'HH:mm'", "end | date: 'dd/MM/yyyy'",'user.name', 'user.lastname'] : ["-end | date: 'HH:mm'", "end | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortSchedule() {
          sortStartSchedule();
        }

        function sortDayStart() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["iin", 'user.name', 'user.lastname', 'iin'] : ["-iin", 'user.name', 'user.lastname', 'iin'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "dayComparator");
        }

        function sortDateStart() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["iin | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'] : ["-iin | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortStart() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["iin | date: 'HH:mm'", "iin | date: 'dd/MM/yyyy'",'user.name', 'user.lastname'] : ["-iin | date: 'HH:mm'", "iin | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortDayEnd() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["out", 'user.name', 'user.lastname', 'out'] : ["-out", 'user.name', 'user.lastname', 'out'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "dayComparator");
        }

        function sortDateEnd() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["out | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'] : ["-out | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortEnd() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["out | date: 'HH:mm'", "out | date: 'dd/MM/yyyy'",'user.name', 'user.lastname'] : ["-out | date: 'HH:mm'", "out | date: 'dd/MM/yyyy'", 'user.name', 'user.lastname'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortHours() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["workedSeconds",'user.name', 'user.lastname'] : ["-workedSeconds", 'user.name', 'user.lastname'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortJustifications() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["justification.identifier",'user.name', 'user.lastname', 'date'] : ["-justification.identifier", 'user.name', 'user.lastname', 'date'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
        }

        function sortNotes() {
          var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ["notes",'user.name', 'user.lastname', 'date'] : ["-notes", 'user.name', 'user.lastname', 'date'];
          AssistanceUtils.clearSort('listSortReports');
          vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
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
              var order = (AssistanceUtils.processSortRev("reverseSortReports")) ? ['user.name', 'user.lastname', 'date'] : ['-user.name', '-user.lastname', 'date'];
              vm.model.statistics = AssistanceUtils.sort(vm.model.statistics, 'listSortReports', order, "localeSensitiveComparator");
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

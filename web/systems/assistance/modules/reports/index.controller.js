(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('ReportsCtrl', ReportsCtrl);

    ReportsCtrl.$inject = ['$scope', 'Assistance', 'Users', '$timeout', 'Login', '$window', 'Offices'];

    function ReportsCtrl($scope, Assistance, Users, $timeout, Login, $window, Offices) {
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
          }
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

        vm.getDayOfWeek = getDayOfWeek;
        vm.getDate = getDate;
        vm.getHour = getHour;
        vm.getUserNames = getUserNames;
        vm.getUserDni = getUserDni;
        vm.getWorkedHours = getWorkedHours;

        $scope.$on('wamp.open', function(event, args) {
          activate();
        });

        activate();



        function activate() {
          if (Login.getPrivateTransport() == null) {
            return
          }
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
          vm.model.search.sTime.setHours(0);
          vm.model.search.sTime.setMinutes(0);
          vm.model.search.sTime.setSeconds(0);
          vm.model.search.sTime.setMilliseconds(0);

          vm.model.search.eTime.setHours(23);
          vm.model.search.eTime.setMinutes(59);
          vm.model.search.eTime.setSeconds(0);
          vm.model.search.eTime.setMilliseconds(0);

          vm.model.header.columns = [];
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
              _initializeFilters();
              vm.findStatistics();
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

        }


        // ***********************************************************************


        function getWorkedHours(seconds) {
          var minutes = ('0' + Math.floor(seconds / 60 % 60)).substr(-2, 2);
          return Math.floor(seconds / 60 / 60) + ':' + minutes;
        }

        function getUserNames(uid) {
          var u = _getUser(uid);
          return u.name + ' ' + u.lastname;
        }

        function getUserDni(uid) {
          return _getUser(uid).dni;
        }

        function _getUser(uid) {
          for (var i = 0; i < vm.model.users.length; i++) {
            if (vm.model.users[i].id == uid) {
              return vm.model.users[i];
            }
          }
          return {
            name: '',
            lastname: '',
            dni: ''
          }
        }

        function getDayOfWeek(date) {
          if (date == null) {
            return '';
          }
          var d = ['Lun', 'Mar', 'Mier', 'Jue', 'Vier', 'Sáb', 'Dom'];
          return d[date.getDay()];
        }

        function getDate(date) {
          if (date == null) {
            return '';
          }
          return Assistance._formatDateDay(date);
        }

        function getHour(date) {
          if (date == null) {
            return '';
          }
          return Assistance._formatDateHour(date);
        }

        function _format(stats) {
          for (var i = 0; i < stats.length; i++) {
            stats[i].date = (stats[i].date != null) ? new Date(stats[i].date) : null;
            stats[i].iin = (stats[i].iin != null) ? new Date(stats[i].iin) : null;
            stats[i].out = (stats[i].out != null) ? new Date(stats[i].out) : null;
          }
        }

        function findStatistics() {
          var dstart = vm.model.search.start;
          var dend = vm.model.search.end;
          vm.model.statistics = [];

          Assistance.getStatistics(dstart, dend, [], vm.model.search.offices).then(function(stats) {
            console.log(stats);
            $timeout(function() {
              var uids = [];
              for (var uid in stats) {
                for (var i = 0; i < stats[uid].length; i++) {
                  uids.push(uid)
                  var ds = stats[uid][i].dailyStats;
                  console.log(ds)
                  vm.model.statistics = vm.model.statistics.concat(ds);
                }
              }
              _format(vm.model.statistics);
              Users.findById(uids).then(function(users) {
                $timeout(function() {
                  vm.model.users = users;
                });
              }, function(err) {
                console.log(err);
              });
            });
          }, function(err) {
            console.log(err);
          });
        }
    }

})();

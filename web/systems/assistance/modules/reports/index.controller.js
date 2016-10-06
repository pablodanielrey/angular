(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('ReportsCtrl', ReportsCtrl);

    ReportsCtrl.$inject = ['$scope', 'Assistance', 'Users', '$timeout'];

    function ReportsCtrl($scope, Assistance, Users, $timeout) {
        var vm = this;

        vm.model = {
          users: {},
          statistics: [],
          search: {
            start: new Date(),
            end: new Date()
          }
        }

        vm.findStatistics = findStatistics;
        vm.getDayOfWeek = getDayOfWeek;
        vm.getDate = getDate;
        vm.getHour = getHour;
        vm.getUserNames = getUserNames;
        vm.getUserDni = getUserDni;
        vm.getWorkedHours = getWorkedHours;

        function getWorkedHours(seconds) {
          return Math.floor(seconds / 60 / 60) + ':' + Math.floor(seconds / 60 % 60);
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

          Assistance.getStatistics(dstart, dend, ['89d88b81-fbc0-48fa-badb-d32854d3d93a']).then(function(stats) {
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

(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('LogsCtrl', LogsCtrl);

    LogsCtrl.$inject = ['$scope', 'Assistance', 'Users'];

    function LogsCtrl($scope, Assistance, Users) {
        var vm = this;

        vm.model = {
          logs: [],
          status: [],
          inside: 0,
          outside: 0
        };

        vm.getLogs = getLogs;

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
              return vm.model.status[i].status;
            }
          }
          vm.model.status.push({id:userId, status:true});
          return true;
        }

        function _parseLog(log, users) {
          var user = _findUser(log.userId, users);
          var cca = _calcStatus(user.id) ? 'entrada' : 'salida';
          var d = new Date(log.log);
          return {
              clase: cca,
              tipo: 'NoDocente',
              name: user.name,
              lastname: user.lastname,
              dni: user.dni,
              dia: _formatDateDay(d),
              hora: _formatDateHour(d)
          }
        }

        function getLogs() {
          var d = new Date()
          Assistance.getLogs(d).then(function(logs) {
            console.log(logs);

            if (logs.length <= 0) {
              return;
            }

            // busco a los usuarios de los logs.
            var uids = _getUsers(logs);
            Users.findById(uids).then(function(users) {

              // seteo los logs y los estados
              var status = [];
              for (var i = 0; i < logs.length; i++) {
                vm.model.logs.push(_parseLog(logs[i], users, status));
              }
              // seteo los valores de los contadores finales.
              vm.model.inside = 0;
              for (var i = 0; i < vm.model.status.length; i++) {
                if (vm.model.status.status) {
                  vm.model.inside = vm.model.inside + 1;
                } else {
                  vm.model.outside = vm.model.outside + 1;
                }
              }


            }, function(err) {
              console.log(err);
            });

          }, function(err) {
            console.log(err);
          })

        }

    };

    function _formatDateDay(d) {
      return d.getDate() + '/' + d.getMonth() + '/' + d.getFullYear()
    }

    function _formatDateHour(d) {
      return d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds();
    }

    function _findUser(uid, users) {
      for (var i = 0; i < users.length; i++) {
        if (users[i].id == uid) {
          return users[i];
        }
      }
      return null;
    }

    function _getUsers(logs) {
      var uids = [];
      for (var i = 0; i < logs.length; i++) {
        uids.push(logs[i].userId);
      }
      return uids;
    }


})();


/*
var app = angular.module('assistance');

app.controller('LogsCtrl', ["$rootScope", '$scope', 'Login',
  function ($rootScope, $scope) {
    var mv = this;

    var nombres = ['Walter Roberto', 'Pablo Daniel', 'Alejandro Agustin', 'Maximiliano Antonio', 'Ivan Roberto'];
    var dnis = ['2738457298', '27294557', '30001823', '12345678', '876554432'];
    var cclase = '';

    $scope.logs = [];


    function getLogs() {
      console.log('getLogs');
    }



    for (var i = 0; i < 100; i++) {
      if (i % 2 == 0) {
        cclase = 'entrada';
      } else {
        cclase = 'salida';
      };

      $scope.logs.push(
        {
          clase: cclase,
          tipo: 'NoDocente',
          name: nombres[i % nombres.length],
          lastname: 'Blanco',
          dni: dnis[i % dnis.length],
          hora: '10:30 am',
          dia: '05/08/2026'
        }
      );
    };


  }
]);
*/

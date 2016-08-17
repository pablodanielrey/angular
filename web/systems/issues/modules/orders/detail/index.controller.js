(function() {
    'use strict';

    angular
        .module('issues')
        .controller('OrdersDetailCtrl', OrdersDetailCtrl);

    OrdersDetailCtrl.$inject = ['$scope', '$routeParams', '$location', 'Login', 'Issues', 'Users'];

    /* @ngInject */
    function OrdersDetailCtrl($scope, $routeParams, $location, Login, Issues, Users) {
        var vm = this;

        // variables del modelo
        vm.model = {
          issue: null, //issue inicial
          users: [], //lista de usuarios participantes de issue y sus hijos
        }



        // variables de la vista
        vm.view = {

        }

        // métodos
        activate();

        function activate() {
          vm.model.userId = Login.getCredentials()['userId'];
          var params = $routeParams;
          vm.model.issue = loadIssue(params.issueId);

        }

        //***** Carga de issue *****
        function loadIssue(id) {
          Issues.findById(id).then(
            function(issue) {
              vm.model.issue = issue;
              var size = (issue.children.length) ? issue.children.length : 0;

              for (var i = 0; i < size; i++) {
                  var child = issue.children[i];
                  loadUser(child.userId); //los usuarios se mantienen en una lista interna
              }
            }, function(error) {
              console.log("Error loadIssue " + error);
            }
          );
        }

        //***** Carga de usuarios *****
        function loadUser(userId) {
          if(!(userId in vm.model.users)) vm.model.users[userId] = null;
          if (!vm.model.users[userId]) {
            Users.findById([userId]).then(
              function(users) { vm.model.users[userId] = users[0];
                console.log(vm.model.users);
              },
              function(error) { console.log("Error loadUser " + error); }
            );
          }
        }


    }
})();

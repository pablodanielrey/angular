(function() {
    'use strict';

    angular
        .module('issues')
        .controller('OrdersDetailCtrl', OrdersDetailCtrl);

    OrdersDetailCtrl.$inject = ['$scope', '$routeParams', '$location', 'Login'];

    /* @ngInject */
    function OrdersDetailCtrl($scope, $routeParams, $location, Login) {
        var vm = this;

        // variables del modelo
        vm.model = {
          selectedIssue = null,
        }



        // variables de la vista
        vm.view = {

        }

        // métodos


        activate();

        function activate() {
          vm.model.userId = Login.getCredentials()['userId']
          var params = $routeParams;

          if (params.issueId == undefined) {
            $location.path('/orders');
          }

          $scope.loadIssue(params.issueId);

        }


        function loadIssue(id) {
          Issues.findById(id).then(
            function(issue) {
              vm.model.selectedIssue = issue;
              //closeMessage();
            }, function(error) {
              //messageError(error);
            }
          );
        }

        function initializeView() {

        }

        function initializeModel() {

        }


    }
})();

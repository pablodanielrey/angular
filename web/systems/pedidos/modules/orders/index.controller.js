angular
  .module('mainApp')
  .controller('OrdersCtrl', OrdersCtrl);

OrdersCtrl.inject = ['$rootScope', '$scope', 'Issue', 'Login', '$timeout', 'Users', 'Office']

function OrdersCtrl($rootScope, $scope, Issue, Login, $timeout, Users, Office) {

  $scope.initialize = initialize;

  $scope.model = {
    userId: null
  }

  $scope.view = {
    style: '',
    style2: ''
  }

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.model.userId = '';
    Login.getSessionData()
      .then(function(s) {
          $scope.model.userId = s.user_id;
          $scope.initialize();
      }, function(err) {
        console.log(err);
      });
  });

  function initialize() {

  }

}

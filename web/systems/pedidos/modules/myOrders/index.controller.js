angular
  .module('mainApp')
  .controller('MyOrdersCtrl', MyOrdersCtrl);

MyOrdersCtrl.inject = ['$rootScope', '$scope', 'Issue', 'Login', '$timeout']

function MyOrdersCtrl($rootScope, $scope, Issue, Login, $timeout) {

  $scope.initialize = initialize;
  $scope.getMyIssues = getMyIssues;

  $scope.model = {
    userId: null
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
    $scope.getMyIssues();
  }

  function getMyIssues() {
    Issue.getMyIssues().then(
        function(issues) {
          console.log(issues);
        },
        function(err) {
          console.log('error')
        }
    );
    
  }

}

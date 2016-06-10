angular
  .module('mainApp')
  .controller('MyOrdersCtrl', MyOrdersCtrl);

MyOrdersCtrl.inject = ['$rootScope', '$scope', 'Issue', 'Login', '$timeout']

function MyOrdersCtrl($rootScope, $scope, Issue, Login, $timeout) {

  $scope.initialize = initialize;
  $scope.getMyIssues = getMyIssues;
  $scope.viewDetail = viewDetail;

  $scope.model = {
    userId: null,
    issues: [],
    issueSelected: null
  }

  $scope.view = {
    style: ''
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
    $scope.model.issues = [];
    $scope.getMyIssues();
  }

  function getMyIssues() {
    Issue.getMyIssues().then(
      function(issues) {
        $scope.$apply(function() {
          $scope.model.issues = issues;
          console.log(issues);
        });

      },
      function(err) {
        console.log('error')
      }
    );
  }

  function viewDetail(issue) {
    $scope.model.issueSelected = issue;
    $scope.view.style = 'pantallaDetallePedido';
  }

}

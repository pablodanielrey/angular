angular
  .module('mainApp')
  .controller('MyOrdersCtrl', MyOrdersCtrl);

MyOrdersCtrl.inject = ['$rootScope', '$scope', 'Issue', 'Login', '$timeout', 'Users']

function MyOrdersCtrl($rootScope, $scope, Issue, Login, $timeout, Users) {

  $scope.initialize = initialize;
  $scope.getMyIssues = getMyIssues;
  $scope.viewDetail = viewDetail;
  $scope.getDate = getDate;
  $scope.getDiffDay = getDiffDay;
  $scope.getStatus = getStatus;
  $scope.getName = getName;

  $scope.create = create;
  $scope.cancel = cancel;
  $scope.save = save;

  $scope.model = {
    userId: null,
    issues: [],
    issueSelected: null
  }

  $scope.view = {
    style: '',
    styles : ['', 'pantallaNuevoPedido','pantallaDetallePedido'],
    status: ['Nueva', 'En curso', 'Finaliza', '', 'Cerrada']
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
          for (var i = 0; i < issues.length; i++) {
            dateStr = issues[i].start;
            dateSplit = dateStr.split('-');
            issues[i].date = new Date(dateSplit[0],dateSplit[1] - 1,dateSplit[2]);
            loadUser(issues[i]);
          }
          $scope.model.issues = issues;
          console.log(issues);
        });

      },
      function(err) {
        console.log('error')
      }
    );
  }

  function loadUser(issue) {
    Users.findById([issue.userId.toString()]).then(
      function(users) {
        issue.user = users[0];
      }
    );
  }

  function viewDetail(issue) {
    $scope.model.issueSelected = issue;
    $scope.view.style = $scope.view.styles[2];
  }

  function create() {
    $scope.model.issue = {};
    $scope.view.style = $scope.view.styles[1];
  }

  function cancel() {
    $scope.model.issue = {};
    $scope.view.style = $scope.view.styles[0];
  }

  function save() {
    $scope.view.style = $scope.view.styles[0];
  }

  function getDate(issue) {
    return issue.date;
  }

  function getDiffDay(issue) {
    now = new Date();
    diff = now - issue.date;
    days = Math.floor(diff / (1000 * 60 * 60 * 24));
    return (days == 0) ? 'Hoy' : (days == 1) ? 'Ayer' : days + ' días'
  }

  function getStatus(issue) {
    return $scope.view.status[issue.statusId - 1];
  }

  function getName(issue) {
    return (issue == null || issue.user == null) ? 'No tiene nombre' : issue.user.name + ' ' + issue.user.lastname;
  }

}

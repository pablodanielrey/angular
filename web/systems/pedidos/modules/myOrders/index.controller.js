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

  $scope.loadOffices = loadOffices;
  $scope.selectOffice = selectOffice;
  $scope.selectArea = selectArea;
  $scope.selectSubject = selectSubject;
  $scope.loadAreas = loadAreas;
  $scope.loadSubjects = loadSubjects;

  $scope.create = create;
  $scope.cancel = cancel;
  $scope.save = save;

  $scope.model = {
    userId: null,
    issues: [],
    issueSelected: null,
    offices: [],
    areas: [],
    subjects: [],
    subject: '',
    description: '',
    selectedOffice: null,
    searchOffice: {name:''},
    searchArea: {name:''},
    selectedArea: null
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
    $scope.loadOffices();
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

  function loadOffices() {
    $scope.model.offices = [];
    Issue.getOffices().then(
      function(offices) {
        $scope.model.offices = offices;
      },
      function(error) {
        console.log(error);
      }
    )
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
    clearOffice();
    $scope.model.description = '';
  }

  function cancel() {
    $scope.model.issue = {};
    $scope.view.style = $scope.view.styles[0];
  }

  function selectOffice(office) {
    clearArea();
    $scope.model.selectedOffice = office;
    $scope.model.searchOffice = (office == null) ? {name:''} : {name: office.name};
    $scope.view.style2 = '';
    loadAreas($scope.model.selectedOffice);
    loadSubjects($scope.model.selectedOffice);
  }

  function clearOffice() {
    $scope.model.selectedOffice = null;
    $scope.model.searchOffice = {name: ''};
    clearArea();
  }

  function clearArea() {
    $scope.model.selectedArea = null;
    $scope.model.searchArea = {name: ''};
    clearSubject();
  }

  function clearSubject() {
    $scope.model.subject = '';
  }

  function selectArea(area) {
    clearSubject();
    $scope.model.selectedArea = area;
    $scope.model.searchArea = (area == null) ? {name:''} : {name: area.name};
    $scope.view.style2 = '';
    loadSubjects($scope.model.selectedArea);
  }

  function loadAreas(office) {
    $scope.model.areas = [];
    Issue.getAreas(office).then(
      function(offices) {
        $scope.model.areas = offices;
      },
      function(error) {
        console.log(error);
      }
    )
  }

  function loadSubjects(office) {
    $scope.model.subjects = ['Otro', 'Wifi'];
  }

  function selectSubject(subject) {
    $scope.model.subject = subject;
    $scope.view.style2 = '';
  }

  function save() {
    var office = ($scope.model.selectedArea != null) ? $scope.model.selectedArea : $scope.model.selectedOffice;
    var subject = $scope.model.subject;
    var description = $scope.model.description;

    if (office == null || $scope.model.subjects.indexOf(subject) < 0) {
      window.alert('Complete los campos correctamente');
      return;
    }

    Issue.create(subject, description, null, office.id).then(
      function(data) {
        $scope.$apply(function() {
          $scope.view.style = $scope.view.styles[0];
          $scope.getMyIssues();
        })
      }, function(error) {
        console.log(error);
      }
    );

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

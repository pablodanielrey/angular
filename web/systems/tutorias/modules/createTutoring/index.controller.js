angular
  .module('mainApp')
  .controller('CreateTutoringCtrl',CreateTutoringCtrl);

CreateTutoringCtrl.inject = ['$rootScope', '$scope'];

function CreateTutoringCtrl($rootScope, $scope) {

  $scope.model = {
    recentTutorings: [],
    recentUsers: []
  }

  $scope.view = {
    style: ''
  }

  $scope.initialize = initialize;
  $scope.loadRecentTutorings = loadRecentTutorings;
  $scope.loadRecentUsers = loadRecentUsers;
  $scope.selectTutoring = selectTutoring;

  function initialize() {
    $scope.loadRecentTutorings();
    $scope.loadRecentUsers();
    console.log("CreateTutoringCtrl");
  }

  function loadRecentTutorings() {
    $scope.model.recentTutorings = [];
    $scope.model.recentTutorings.push({'date':'26/03/2016','day':'Martes'});
    $scope.model.recentTutorings.push({'date':'02/03/2016','day':'Miércoles'});
    $scope.model.recentTutorings.push({'date':'24/02/2016','day':'Viernes'});
    $scope.model.recentTutorings.push({'date':'20/02/2016','day':'Lunes'});
  }

  function loadRecentUsers() {
    $scope.model.recentUsers = [];
    $scope.model.recentUsers.push({'img':'img/pablosarmieto.jpg','name':'Pablo','lastname':'Sarmiento','dni':'30235968'});
    $scope.model.recentUsers.push({'img':'img/lucas.jpg','name':'Lucas','lastname':'Langoni','dni':'35456923'});
    $scope.model.recentUsers.push({'img':'img/walter.jpg','name':'Walter','lastname':'Blanco','dni':'30001823'});
    $scope.model.recentUsers.push({'img':'img/pablo.jpg','name':'Pablo Daniel','lastname':'Rey','dni':'28356952'});
  }

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });


  function selectTutoring(t) {
    $scope.view.style = 'nuevaTutoria';
  }

}

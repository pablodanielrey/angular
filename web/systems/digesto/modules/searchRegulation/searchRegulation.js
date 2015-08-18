angular
    .module('mainApp')
    .controller('SearchRegulationCtrl',SearchRegulationCtrl)

SearchRegulationCtrl.$inject = ['$rootScope','$scope','Digesto','Notifications','$location']

function SearchRegulationCtrl($rootScope,$scope,Digesto,Notifications,$location) {

  $scope.model = {
    searchText: '',
    normatives: []
  }

  $scope.initialize = initialize;
  $scope.find = find;
  $scope.loadNames = loadNames;
  $scope.view = view;
  $scope.edit = edit;

  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  function initialize() {
    $scope.model.searchText = "";
    $scope.model.normatives = [];
  }

  function find() {
    text = $scope.model.searchText;
    if (text.trim() == "") {
      return
    }
    $scope.model.normatives = [];
    Digesto.findNormative(text,null,
        function(normatives) {
          $scope.loadNames(normatives);
          $scope.model.normatives = normatives;
        }, function(error) {
          Notifications.message(error);
        }
    );
  }

  function loadNames(normatives) {
    for (var i = 0; i < normatives.length; i++) {
      normatives[i].status.name = getStatusName(normatives[i].status);
      normatives[i].visibility.name = getVisibilityName(normatives[i].visibility);
    }
  }

  function getStatusName(status) {
    switch (status.status) {
      case 'APPROVED': return 'Aprobada';break;
      case 'PENDING': return 'Pendiente';break;
    }
  }

  function getVisibilityName(visibility) {
    switch (visibility.type) {
      case 'PUBLIC': return 'Público';break;
      case 'PRIVATE': return 'Privado';break;
      case 'GROUPPRIVATE': return 'Privado de Grupo';break;
    }
  }

  function view(normative) {
    $location.path('/load/' + normative.id + '/operation/view');
  }

  function edit(normative) {
    var operation = 'edit';
    $location.path('/load/' + normative.id + '/operation/edit');
  }

}

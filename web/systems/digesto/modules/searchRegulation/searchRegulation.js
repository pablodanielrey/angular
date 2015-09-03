angular
    .module('mainApp')
    .controller('SearchRegulationCtrl',SearchRegulationCtrl)

SearchRegulationCtrl.$inject = ['$rootScope','$scope','$filter','Digesto','Notifications','$location']

function SearchRegulationCtrl($rootScope,$scope,$filter,Digesto,Notifications,$location) {

  $scope.model = {
    searchText: '',
    normatives: []
  }

  $scope.view = {
    reverseType: false,
    reverseNumber: false,
    reverseExp: false,
    reverseIssuer: false,
    reverseState: false,
    reverseVisibility: false
  }

  $scope.initialize = initialize;
  $scope.find = find;
  $scope.loadNames = loadNames;
  $scope.view = view;
  $scope.edit = edit;
  $scope.order = order;



  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  function initialize() {
    $scope.view.reverseType = false;
    $scope.view.reverseNumber = false;
    $scope.view.reverseExp = false;
    $scope.view.reverseIssuer = false;
    $scope.view.reverseState = false;
    $scope.view.reverseVisibility = false;

    $scope.model.searchText = "";
    $scope.model.normatives = [];
  }

  function order(predicate, reverse) {
    $scope.model.normatives = $filter('orderBy')($scope.model.normatives, predicate, reverse);

  };

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
          $scope.order(['type','file_number','normative_number_full','issuer.name','status.name','visibility.name'],view.reverseType);
        }, function(error) {
          Notifications.message(error);
        }
    );
  }

  function loadNames(normatives) {
    for (var i = 0; i < normatives.length; i++) {
      normatives[i].status.name = getStatusName(normatives[i].status);
      normatives[i].visibility.name = getVisibilityName(normatives[i].visibility);
      normatives[i].file_number = (isNaN(normatives[i].file_number))?normatives[i].file_number:parseInt(normatives[i].file_number);
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
    var hashId = window.btoa(normative.id);
    var hashOperation = window.btoa('view');
    $location.path('/load/' + hashId + '/operation/' + hashOperation);
  }

  function edit(normative) {
    var hashId = window.btoa(normative.id);
    var hashOperation = window.btoa('edit');
    $location.path('/load/' + hashId + '/operation/' + hashOperation);
  }

}

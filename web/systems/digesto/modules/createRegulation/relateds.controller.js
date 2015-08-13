angular
    .module('mainApp')
    .controller('RelatedsCtrl',RelatedsCtrl)

    RelatedsCtrl.$inject = ['$rootScope','$scope','Digesto','Notifications']

function RelatedsCtrl($rootScope,$scope,Digesto,Notifications) {
  $scope.initialize = initialize;
  $scope.find = find;
  $scope.selectRelated = selectRelated;

  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  $scope.$on('openRelatedsViewEvent',function(event) {
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
          $scope.$emit('viewSearchResultRelatedsLoad');
          for (var i = 0; i < normatives.length; i++) {
            var include = false;
            for (var j = 0; j < $scope.model.normative.relatedsObj.length; j++) {
              if (normatives[i].id == $scope.model.normative.relatedsObj[j].id) {
                include = true;
              }
            }
            if (!include) {
              $scope.model.normatives.push(normatives[i]);
            }
          }

        }, function(error) {
          Notifications.message(error);
        }
    );
  }

  function selectRelated(normative) {
    $scope.$emit('selectRelated',normative);
  }
}

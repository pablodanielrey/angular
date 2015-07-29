angular
    .module('mainApp')
    .controller('CreateRegulationCtrl',CreateRegulationCtrl);

CreateRegulationCtrl.$inject = ['$rootScope', '$scope', '$location', '$window', '$timeout','WebSocket', 'Session', 'Cache'];

function CreateRegulationCtrl($rootScope, $scope, $location, $window, $timeout, WebSocket, Session, Cache) {

    $scope.model = {
      regulationIndex: 0,
      regulationName: ['','ORDENANZA','RESOLUCIÓN','DISPOSICIÓN','ORDENANZA','RESOLUCIÓN','DISPOSICIÓN',''],
      styleNames: ['menu','screenOrdenanza','screenResolucion','screenDisposicion','screenOrdenanzaFinal','screenResolucionFinal','screenDisposicionFinal']
    };


    $scope.selectRegulation = function(i) {
        $scope.model.regulationIndex = i;
        console.log($scope.model.regulationIndex);
    }

    $scope.getRegulationName = function() {
      var t = $scope.model.regulationName[$scope.model.regulationIndex];
      console.log(t);
      return t;
    }

    $scope.getStyleName = function() {
      var t = $scope.model.styleNames[$scope.model.regulationIndex];
      console.log(t);
      return t;
    }

    $scope.save = function() {
      $scope.model.regulationIndex = $scope.model.regulationIndex + 3;
      console.log($scope.model.regulationIndex);
    }

    $scope.$on('$viewContentLoaded', function(event){
      $scope.model.contentGroupsView = false;
    });

};

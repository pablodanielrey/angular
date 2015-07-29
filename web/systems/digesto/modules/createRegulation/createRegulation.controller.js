angular
    .module('mainApp')
    .controller('CreateRegulationCtrl',CreateRegulationCtrl);

CreateRegulationCtrl.$inject = ['$rootScope', '$scope', '$location', '$window', '$timeout','WebSocket', 'Session', 'Cache', 'Notifications', 'Digesto'];

function CreateRegulationCtrl($rootScope, $scope, $location, $window, $timeout, WebSocket, Session, Cache, Notifications, Digesto) {

    $scope.model = {
      regulationIndex: 0,
      regulationName: ['','ORDENANZA','RESOLUCIÓN','DISPOSICIÓN',''],
      styleNames: ['item1Seleccionado','item2Seleccionado','item2Seleccionado','item2Seleccionado','item3Seleccionado']
    };


    $scope.selectRegulation = function(i) {
        $scope.model.regulationIndex = i;
    }

    $scope.getRegulationName = function() {
      return $scope.model.regulationName[$scope.model.regulationIndex];
    }

    $scope.getStyleName = function() {
      return $scope.model.styleNames[$scope.model.regulationIndex];
    }

    $scope.save = function() {
      normative = {};
      status = "";
      visibility = {};
      relateds = [];
      file = {};
      Digesto.createNormative(normative,status,visibility,relateds,file,
        function(response) {
          Notifications.message(response);
        },
        function(error) {
            Notifications.message(error);
        }
      );
    }

    $scope.$on('$viewContentLoaded', function(event){
      $scope.model.contentGroupsView = false;
    });

};

var app = angular.module('mainApp');

app.controller('MenuDigestoCtrl', ["$rootScope", '$scope', "$location", "$timeout", "$window", "Notifications", "Session", "WebSocket",

  function ($rootScope, $scope, $location, $timeout, $window, Notifications, Session, WebSocket) {

    $scope.model = {
      class:'',
      items: [
        { item: 'Cargar', url: '#/load' },
        { item: 'Buscar', url: '#/search' }

      ]
    }

    $scope.changeContent = function(content) {
      if ($scope.model.class =='') {
        $scope.model.class = content;
      } else {
        $scope.model.class = '';
      }

      console.log(content);
    }
  }
]);

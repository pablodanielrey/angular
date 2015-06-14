var app = angular.module('mainApp');

app.controller('MenuDigestoCtrl', ["$rootScope", '$scope', "$location", "$timeout", "$window", "Notifications", "Session", "WebSocket",

  function ($rootScope, $scope, $location, $timeout, $window, Notifications, Session, WebSocket) {

    $scope.model = {
      items: [
        { item: 'Cargar', url: '#/load' },
        { item: 'Buscar', url: '#/search' }
      ]
    }


  }
]);

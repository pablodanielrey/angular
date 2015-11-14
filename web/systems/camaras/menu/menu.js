var app = angular.module('mainApp');

app.controller('MenuCamerasCtrl', ["$rootScope", '$scope', "$location", "$timeout", "$window", "Notifications", "Session", "WebSocket",

  function ($rootScope, $scope, $location, $timeout, $window, Notifications, Session, WebSocket) {

    $scope.model = {
      class:'',
      items: [
        { name: 'en VIVO!',img:'fa fa-video-camera', url: '#/live' },
        { name: 'Grabaciones',img:'fa fa-youtube-play', url: '#/rec' },



      ],
      cerrado : false
    }

    $scope.toggleMenu = function() {
      $scope.model.cerrado = !$scope.model.cerrado;
    }

  }
]);

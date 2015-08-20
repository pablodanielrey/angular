var app = angular.module('mainApp');

app.controller('rec', function($scope,$timeout) {

    $scope.model = {
      class:'',
      contentRecordings:false,
      rate: 1
    };


    $scope.$on('$viewRecordings', function(event) {
      $scope.model.contentRecordings = false;
    });
    // console.log('hola');

    $scope.pause = function() {
      $scope.model.rate = 1;
      var video = document.getElementById("video");
      video.playbackRate = $scope.model.rate;
      //video.play();
    }

    $scope.faster = function() {
      $scope.model.rate = $scope.model.rate + 0.5;
      var video = document.getElementById("video");
      video.playbackRate = $scope.model.rate;

      if ($scope.model.rate > 0) {
        video.play();
      }
    }

    $scope.slower = function() {
      var video = document.getElementById("video");
      $scope.model.rate = $scope.model.rate - 0.5;

      if ($scope.model.rate < 0) {
        $scope.model.rate = 0;
        video.pause();
      }

      video.playbackRate = $scope.model.rate;
    }

    $scope.seekForward = function() {
      $scope.model.rate = 1;
      var video = document.getElementById("video");
      video.currentTime = video.currentTime + 1;
      video.playbackRate = $scope.model.rate;
      video.pause();
    }

    $scope.seekBackwards = function() {
      $scope.model.rate = 1;
      var video = document.getElementById("video");
      video.currentTime = video.currentTime - 1;
      video.playbackRate = $scope.model.rate;
      video.pause();
    }

  }
);

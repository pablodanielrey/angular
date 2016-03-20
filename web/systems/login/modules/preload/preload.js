
angular
  .module('mainApp')
  .controller('PreloadCtrl',PreloadCtrl)
  .config(function($wampProvider) {
    if (config.url == undefined || config.url == 'autodetect') {
      var conn = {
        url: "ws://" + location.host + ":8000/ws",
        realm: config.realm
      };
      console.log(conn);
      $wampProvider.init(conn);
    } else {
      var conn = {
        url: config.url,
        realm: config.realm
      };
      console.log(conn);
      $wampProvider.init(conn);
    }
  })
  .run(function($wamp) {
    $wamp.open();
  });

PreloadCtrl.$inject = ['$scope','$window','$interval','Login','Users'];

function PreloadCtrl($scope, $window, $interval, Login, Users) {

  $scope.logged = false;
  $scope.percent = 0;

  $scope.doLogged = function() {
    $scope.logged = true;
  }

  $scope.getLoggedClazz = function() {
    if ($scope.logged) {
      return 'logged';
    } else {
      return 'noLogged';
    }
  }

  $scope.initialize = function() {
    $scope.logged = Login.isLogged();
  }
  console.log('preload cargado');

  $scope.interval = $interval(function() {
    console.log('progreso');
    $scope.percent = $scope.percent + 1;
    if ($scope.percent >= 100) {
      $interval.cancel();
      $scope.logged = true;
    }
  }, 100, [100]);

  $scope.$on('$viewContentLoaded', function(event) {
    //$scope.initialize();

  });


}

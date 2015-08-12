var app = angular.module('mainApp');

app.controller('MenuCtrl', ["$rootScope", '$scope', '$location', 'Notifications',

  function ($rootScope, $scope, $location, $window, $http, Profiles, Session, Notifications) {

    $scope.model = {
      class:'',
      items: []
    }

    $scope.toggleMenu = function() {
      $scope.$parent.model.hideMenu = !$scope.$parent.model.hideMenu;
    }

    $scope.download = function() {
      $location.path('/download');
    }

    $scope.upload = function() {
      $location.path('/upload');
    }

  	$scope.exit = function() {
  		$location.path('/logout');
  	}

    var compare = function(a,b) {
      return a.n - b.n;
    }

    $scope.initialize = function() {
      $scope.model.items = [];
      $scope.model.items.push({ n:1, label:'Descargar', img:'fa fa-lock', function: $scope.download });
      $scope.model.items.push({ n:1, label:'Inscribirse', img:'fa fa-lock', function: $scope.upload });
    }

    $rootScope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });


  }
]);

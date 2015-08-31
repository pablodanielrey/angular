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
      $location.path('/descargar');
    }

    $scope.upload = function() {
      $location.path('/inscripcion');
    }

  	$scope.exit = function() {
  		$location.path('/logout');
  	}

    var compare = function(a,b) {
      return a.n - b.n;
    }

    $scope.initialize = function() {
      $scope.model.items = [];
      $scope.model.items.push({ n:1, label:'Inscripción', img:'fa fa-lock', function: $scope.upload });
      $scope.model.items.push({ n:1, label:'Descargar', img:'fa fa-lock', function: $scope.download });

    }

    $rootScope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });


  }
]);

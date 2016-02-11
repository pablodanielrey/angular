var app = angular.module('mainApp');

app.controller('MenuCtrl', ["$rootScope", '$scope', '$location', 'Notifications', 'Login',

  function ($rootScope, $scope, $location, Notifications, Login) {

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

    $scope.search = function() {
      $location.path('/busqueda');
    }

  	$scope.exit = function() {
      var sid = '';
      Login.logout(sid, function(ok) {
        $location.path('/');
      }, function(err) {
        console.log(err)
        Notifications.message(err);
      });
  	}

    var compare = function(a,b) {
      return a.n - b.n;
    }

    $scope.initialize = function() {
      $scope.model.items = [];
      $scope.model.items.push({ n:1, label:'Inscripción', img:'fa fa-ticket', function: $scope.upload });
      $scope.model.items.push({ n:1, label:'Busqueda', img:'fa fa-search', function: $scope.search });
      //$scope.model.items.push({ n:1, label:'Descargar', img:'fa fa-lock', function: $scope.download });
      $scope.model.items.push({ n:1, label:'Salir', img:'fa fa-sign-out', function: $scope.exit });

    }

    $rootScope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });


  }
]);

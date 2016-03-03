var app = angular.module('mainApp');

app.controller('MenuCtrl', ["$rootScope", '$scope', '$location', 'Notifications', 'Login', 'Session',

  function ($rootScope, $scope, $location, Notifications, Login, Session) {

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
      var sid = Session.getCurrentSession();
      Login.logout(function(ok) {
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

      var uid = Login.getUserId();
      if (uid == '9c5cf510-cc0d-4cc2-83e5-e61e3e39be58' ||  // paula
          uid == 'f4db8211-55e0-4adf-8443-72fed94cc1b0' ||  // lucas
          uid == '89d88b81-fbc0-48fa-badb-d32854d3d93a' ||  // pablo
          uid == '205de802-2a15-4652-8fde-f23c674a1246' // walter
        ) {
        $scope.model.items.push({ n:1, label:'Busqueda', img:'fa fa-search', function: $scope.search });
        //$scope.model.items.push({ n:1, label:'Descargar', img:'fa fa-lock', function: $scope.download });
      }
      $scope.model.items.push({ n:1, label:'Salir', img:'fa fa-sign-out', function: $scope.exit });

    }

    $rootScope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });


  }
]);

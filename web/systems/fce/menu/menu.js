var app = angular.module('mainApp');

app.controller('MenuCtrl', ["$rootScope", '$scope', '$location', '$window', '$http','Profiles', 'Session', 'Notifications',

  function ($rootScope, $scope, $location, $window, $http, Profiles, Session, Notifications) {

    $scope.model = {
      class:'',
      items: []
    }

    $scope.toggleMenu = function() {
      $scope.$parent.model.hideMenu = !$scope.$parent.model.hideMenu;
    }



    /*
      Funciones de activación de los items del menu
    */

    $scope.myProfile = function() {
  		// selecciono para que toda la funcionalidad de myData funcione sobre el usuario logueado.
  		var s = Session.getCurrentSession();
  		s.selectedUser = s.user_id;
  		Session.saveSession(s);
  	}

  	$scope.changePassword = function() {
  		$location.path('/changePassword');
  	}

    $scope.webmail = function() {
        //$window.open('http://webmail.econo.unlp.edu.ar', 'nnt');
/*        $http(
        {
          method:'POST',
          url: 'https://webmail.econo.unlp.edu.ar/src/redirect.php',
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          },
          data: {
              login_username: 'usuario',
              secretkey: 'clave',
              js_autodetect_results: '0',
              just_logged_in: '0'
            },
          headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }, 'nnt'
      ).success(function(response) {

          console.log(response);
      });
      */

      $window.open('http://webmail.econo.unlp.edu.ar', 'nnt');
      setTimeout( function() {
        $window.document.getElementById('nnt').contentWindow.document.getElementsByName('login_username').value = 'usuario';
        $window.document.getElementById('nnt').contentWindow.document.getElementsByName('secretkey').value = 'clave';
        $window.document.getElementById('nnt').contentWindow.document.getElementsByName('login_form')[0].submit();
      }, 5000);
    }

    $scope.au24 = function() {
        $window.open('http://www.au24.econo.unlp.edu.ar', 'nnt');
  	}

  	$scope.editUsers = function() {

  	}

  	$scope.accountRequests = function() {
  	}

  	$scope.assistance = function() {
  	}

  	$scope.office = function() {
  		//$window.location.href = "/systems/offices/";
  	  //$window.open('/systems/offices/', '_blank');
      $window.open('/systems/offices/', 'nnt');
  		// $window.open('http://127.0.0.1:8000/systems/offices/', '_blank');
  	}

  	$scope.exit = function() {
  	  $window.location.href = "/systems/login/#/logout";
  	}

  	$scope.tutors = function() {
  		$location.path('/tutors');
  	}


    var compare = function(a,b) {
      return a.n - b.n;
    }


    $scope.initialize = function() {

      $scope.model.items = [];

      $scope.model.items.push({ n:40, label:'WebMail', img:'fa fa-lock', function: $scope.webmail });
      $scope.model.items.push({ n:30, label:'Au24', img:'fa fa-lock', function: $scope.au24 });

  		Profiles.checkAccess(Session.getSessionId(),['ADMIN'], function(ok) {

  			if (ok) {
  				$scope.model.items.push({ n:1, label:'Mis datos', img:'fa fa-pencil-square-o', function: $scope.myProfile });
  				$scope.model.items.push({ n:2, label:'Cambiar clave', img:'fa fa-lock', function: $scope.changePassword });
  				$scope.model.items.push({ n:3, label:'Editar usuarios', img:'fa fa-users', function: $scope.editUsers });
  				$scope.model.items.push({ n:4, label:'Pedidos de cuentas', img:'fa fa-inbox', function: $scope.accountRequests });
  				$scope.model.items.push({ n:100, label:'Salir', img:'fa fa-sign-out', function: $scope.exit });

  			} else {
  				$scope.model.items.push({ n:1, label:'Mis datos', img:'fa fa-pencil-square-o', function: $scope.myProfile });
  				$scope.model.items.push({ n:2, label:'Cambiar clave', img:'fa fa-lock', function: $scope.changePassword });
  				$scope.model.items.push({ n:100, label:'Salir', img:'fa fa-sign-out', function: $scope.exit });
  			}
        $scope.model.items.sort(compare);
  		},
  		function(error) {
  		    Notifications.message(error);
  		});

  		Profiles.checkAccess(Session.getSessionId(),['ADMIN-TUTOR','USER-TUTOR'], function(ok) {
  			if (ok) {
  				$scope.model.items.push({ n:10, label:'Tutorias', img:'fa fa-pencil-square-o', function: $scope.tutors });
  			}
        $scope.model.items.sort(compare);
  		},
  		function(error) {
  		    Notifications.message(error);
  		});

  		Profiles.checkAccess(Session.getSessionId(),['ADMIN-ASSISTANCE','USER-ASSISTANCE'], function(ok) {
  			if (ok) {
  				$scope.model.items.push({ n:20, label:'Asistencia', img:'fa fa-clock-o', function: $scope.assistance });
  			}
        $scope.model.items.sort(compare);
  		},
  		function(error) {
  			Notifications.message(error);
  		});

  		Profiles.checkAccess(Session.getSessionId(),['ADMIN-OFFICES','USER-OFFICES'], function(ok) {
  			if (ok) {
  				$scope.model.items.push({ n:30, label:'Oficinas', img:'fa fa-clock-o', function: $scope.office });
  			}
        $scope.model.items.sort(compare);
  		},
  		function(error) {
  			Notifications.message(error);
  		});

      /*
      { name: 'Crear Norma', img:'fa fa-file-text', url: '#/load' },
      { name: 'Buscar Norma', img:'fa fa fa-search', url: '#/search' }*/

    }

    $rootScope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });


  }
]);

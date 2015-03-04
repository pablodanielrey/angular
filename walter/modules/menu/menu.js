

var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, $location, $timeout, Session, Utils, Profiles) {

	$scope.showSubOptions = false;

	$scope.showSubOptionsMenu = function() {
		return $scope.showSubOptions;
	}


	$scope.myProfile = function() {

		// selecciono para que toda la funcionalidad de myData funcione sobre el usuario logueado.
		var s = Session.getCurrentSession();
		s.selectedUser = s.user_id;
		Session.saveSession(s);

		$scope.showSubOptions = true;
		$rootScope.$broadcast("MenuOptionSelectedEvent",'MyDataOption');
	}

	$scope.changePassword = function() {
		$rootScope.$broadcast("MenuOptionSelectedEvent",'ChangePasswordOption');		// esto lo realizo para que los otros menus se cierren.
		$location.path('/changePassword');
	}

	$scope.editUsers = function() {
		$scope.showSubOptions = true;
		$rootScope.$broadcast("MenuOptionSelectedEvent",'EditUsersOption');
	}

	$scope.accountRequests = function() {
		$scope.showSubOptions = true;
		$rootScope.$broadcast("MenuOptionSelectedEvent",'AccountRequestsOption');
	}

	$scope.exit = function() {
		$rootScope.$broadcast("MenuOptionSelectedEvent",'LogoutOption');		// esto lo realizo para que los otros menus se cierren.
		$location.path('/logout');
	}

	$scope.items = [];

	// se generan por los distintos perfiles de usuarios.
	$scope.generateItems = function() {
		Profiles.checkAccess(Session.getSessionId(),'ADMIN', function(ok) {

			if (ok == 'granted') {
				$scope.items = [];
				$scope.items.push({ label:'Mis datos', img:'fa-pencil-square-o', function: $scope.myProfile });
				$scope.items.push({ label:'Cambiar clave', img:'fa-lock', function: $scope.changePassword });
				$scope.items.push({ label:'Editar usuarios', img:'fa-users', function: $scope.editUsers });
				$scope.items.push({ label:'Pedidos de cuentas', img:'fa-inbox', function: $scope.accountRequests });
				$scope.items.push({ label:'Asistencia', img:'fa-clock-o', function: $scope.Assistance });
				$scope.items.push({ label:'Salir', img:'fa-sign-out', function: $scope.exit });
				$scope.itemsGenerated = true;
			} else {

				$scope.items = [];
				$scope.items.push({ label:'Mis datos', img:'fa-pencil-square-o', function: $scope.myProfile });
				$scope.items.push({ label:'Cambiar clave', img:'fa-lock fa-spin', function: $scope.changePassword });
				$scope.items.push({ label:'Salir', img:'fa-sign-out', function: $scope.exit });
				$scope.itemsGenerated = true;
			}

		},
		function(error) {
			alert(error);
		});
	}

	$scope.itemSelected = null;

	$scope.selectItem = function(i) {
		$location.path('/');
		$scope.showSubOptions = false;
		$scope.itemSelected = i;
		i.function();
	}

	/**
	* Esta seleccionado el item del menu enviado como parametro?
	*/
	$scope.isItemSelected = function(i){
		return ($scope.itemSelected == i);
	}


	$scope.$on('LoginEvent',function(event,data) {
		$scope.generateItems();
	});



});

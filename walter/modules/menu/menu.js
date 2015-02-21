

var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, $location, Session, Utils) {

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


	$scope.items = [
		{ label:'Mis datos', img:'fa-pencil-square-o', function: $scope.myProfile },
		{ label:'Cambiar clave', img:'fa-lock', function: $scope.changePassword },
		{ label:'Editar usuarios', img:'fa-users', function: $scope.editUsers },
		{ label:'Pedidos de cuentas', img:'fa-inbox', function: $scope.accountRequests },
		{ label:'Salir', img:'fa-sign-out', function: $scope.exit }
	];


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


});

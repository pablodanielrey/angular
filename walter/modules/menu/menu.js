

var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, $location, Session, Utils) {

	$scope.myProfile = function() {
		$rootScope.$broadcast("MenuOptionSelectedEvent",'MyDataOption');
	}

	$scope.changePassword = function() {
		$rootScope.$broadcast("MenuOptionSelectedEvent",'ChangePasswordOption');		// esto lo realizo para que los otros menus se cierren.
		$location.path('/changePassword');
	}

	$scope.editUsers = function() {
		$rootScope.$broadcast("MenuOptionSelectedEvent",'EditUsersOption');
	}

	$scope.accountRequests = function() {
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

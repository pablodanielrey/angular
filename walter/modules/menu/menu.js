

var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, $location, Session, Utils) {

	$scope.myProfile = function() {
		$rootScope.$broadcast("MenuOptionSelectedEvent",'MyProfileOption');
	}

	$scope.changePassword = function() {
		alert("2");
	}

	$scope.editUsers = function() {
		alert("3");
	}

	$scope.accountRequests = function() {
		$rootScope.$broadcast("MenuOptionSelectedEvent",'AccountRequestsOption');
	}

	$scope.exit = function() {
		alert("5");
	}


	$scope.items = [
		{ label:'Mis datos', img:'fa-pencil-square-o', function: $scope.myProfile },
		{ label:'Cambiar clave', img:'fa-lock', url:'changePassword', function: $scope.changePassword },
		{ label:'Editar usuarios', img:'fa-users', url:'editUsers', function: $scope.editUsers },
		{ label:'Pedidos de cuentas', img:'fa-inbox', url:'accountRequestEdit', function: $scope.accountRequests },
		{ label:'Salir', img:'fa-sign-out', url:'logout', function: $scope.exit }
	];


	$scope.itemSelected = null;

	$scope.selectItem = function(i) {
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

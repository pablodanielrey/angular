

var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, $location, Session) {

	$scope.secondItems = [];
	$scope.selectedItemIndex = null;
	$scope.selectedSecondItemIndex = null;
	$scope.secondVisible = false;
	$scope.secondMenuVisible = false;
	$scope.userListVisible = false;
	$rootScope.userId = null;

	/**
	* Cargar indice del elemento seleccionado
	*/
	$scope.itemClicked = function ($index) {
		$scope.selectedItemIndex = $index;
		$scope.selectedSecondItemIndex = null;
		$location.url("");
		$rootScope.userId = null;
	};
	
	/**
	 * Cargar indice del segundo elemento seleccionado
	 */
	$scope.secondItemClicked = function ($index) {
		$scope.selectedSecondItemIndex = $index;
	};


	/**
	 * Accion por defecto de los items
	 */
	var defaultActionItem = function(){
		$scope.secondItems = [];
		$scope.secondVisible = false;
		var item = $scope.items[$scope.selectedItemIndex];
		if(item.url != undefined){
			$location.url(item.url);
		}
	};
	
	/**
	 * Accion por defecto de los second items
	 */
	var defaultActionSecondItem = function(){
		var secondItem = $scope.secondItems[$scope.selectedSecondItemIndex];
		if(secondItem.url != undefined){
			$location.url(secondItem.url);
		}
	};
	
	var editProfile = function() {
		$scope.secondItems = [
			{label:'Perfil', img:'fa-user', url:'editUserProfile', function: defaultActionSecondItem },
			{label:'Datos de Alumno', img:'fa-university', url:'editStudent', function: defaultActionSecondItem },
			{label:'Au24', img:'fa-th-large', url:'#', function: defaultActionSecondItem },
			{label:'Inserción Laboral', img:'fa-th-large', url:'#', function: defaultActionSecondItem }
		];

		$scope.userListVisible = false;
		$scope.secondVisible = true;
		$scope.secondMenuVisible = true;
	};


	/**
	 * Activar submenu de edicion de usuarios
	 */
	var editUsers = function(){
		$scope.secondVisible = true;
		$scope.secondMenuVisible = false;
		$scope.userListVisible = true;
	};

	$scope.items = [
		{label:'Mis datos', img:'fa-pencil-square-o', function: editProfile },
		{label:'Cambiar clave', img:'fa-lock', url:'changePassword', function: defaultActionItem },
		{label:'Editar usuarios', img:'fa-users', url:'editUsers', function: editUsers },
		{label:'Pedidos de cuentas', img:'fa-inbox', url:'listAccountRequests', function: defaultActionItem },
		{label:'Salir', img:'fa-sign-out', url:'logout', function: defaultActionItem }
	];
	
	var ep = editProfile;
	$scope.$on('UserSelectedEvent', function(event,userId) {
		if($scope.userListVisible){
			ep();
		}
		$rootScope.userId = userId;
	});
	

});

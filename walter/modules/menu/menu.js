

var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, $location, Session, Utils) {

	var selectedItemId = null; //id del item del menu seleccionado
	var menuItemActive = null; //item  del menu activo
	
	var submenuMain = false; //flag para indicar la visualizacion del submenu principal
	var submenuUser = false; //flag para indicar la visualizacion del submenu de usuarios
	var submenuAccount = false; //flag para indicar la visualizacion del submenu de cuentas
	
	var selectedSubmenuItemId = null; //id del item del submenu seleccionado
	var submenuItemActive = null; //item activo del submenu
	
	
	//inicializar items del submenu principal
	$scope.submenuItems = []; 
	
	
	var initializeAllSubmenu = function(){
		initializeSubmenuMain();
		initializeSubmenuUser();
		initializeSubmenuAccount();
	}
	
	var showSubmenuMain = function(){
		initializeAllSubmenu();
		submenuMain = true;
	}
	
	var showSubmenuUser = function(){
		initializeAllSubmenu();
		submenuUser = true;
	}
	
	var showSubmenuAccount = function(){
		initializeAllSubmenu();
		submenuAccount = true;
	}
	
	
	/**
	 * Inicializar submenu
	 */
	var initializeSubmenuMain = function(){
		selectedSubmenuItemId = null;
		submenuItemActive = null;
		submenuMain = false;
	};
	
	var initializeSubmenuUser = function(){
		submenuUser = false;
		$rootScope.userId = null;
	}
	
	var initializeSubmenuAccount = function(){
		submenuAccount = false;
	}
	
	/**
	 * Esta activo el submenu principal?
	 */
	$scope.isSubmenuMain = function(){
		return submenuMain;
	}
	 
	/**
	 * Esta activo el submenu de usuarios?
	 */
	$scope.isSubmenuUser = function(){
		return submenuUser;
	}
	 
	 /**
	 * Esta activo el submenu de cuentas?
	 */
	 $scope.isSubmenuAccount = function(){
		return submenuAccount;
	 }
	 
	
	
	 	 

	/**
	 * Seleccionar item del menu principal
	 */
	$scope.selectItem = function (itemId){
		//inicializar variables del menu
		selectedItemId = itemId;

		//inicializar submenus
		initializeAllSubmenu();
		
		//inicializar interface de visualizacion
		$location.url("");
		
		//buscar item seleccionado
		menuItemActive = Utils.filter(function(element) {
			return element.id == itemId;
		}, $scope.items)[0];
		
		//ejecutar funcion del item seleccionado
		menuItemActive.function();
	};
	
	
	/**
	 * Seleccionar item del submenu principal
	 */
	$scope.selectSubmenuItem = function(itemId){
		//inicializar variables del menu
		selectedSubmenuItemId = itemId;
		
		//inicializar interface de visualizacion
		$location.url("");
		
		//buscar item seleccionado
		submenuItemActive = Utils.filter(function(element) {
			return element.id == itemId;
		}, $scope.submenuItems)[0];
		
		//ejecutar funcion del item seleccionado
		submenuItemActive.function();
	};
	
	/**
	 * Accion por defecto del submenu
	 */
	var defaultActionMenu = function(){
		if(menuItemActive.url != undefined){
			$location.url(menuItemActive.url);
		}
	};
	
	
	/**
	 * Accion por defecto del submenu
	 */
	var defaultActionSubmenu = function(){
		if(submenuItemActive.url != undefined){
			$location.url(submenuItemActive.url);
		}
	};
	
	var editProfile = function() {
		$scope.submenuItems = [
			{id:'user', label:'Perfil', img:'fa-user', url:'editUserProfile', function: defaultActionSubmenu },
			{id:'student', label:'Datos de Alumno', img:'fa-university', url:'editStudent', function: defaultActionSubmenu },
			{id:'au24', label:'Au24', img:'fa-th-large', url:'#', function: defaultActionSubmenu },
			{id:'job', label:'Inserción Laboral', img:'fa-th-large', url:'#', function: defaultActionSubmenu }
		];

		showSubmenuMain();
	};
	
	
	/**
	 * Esta seleccionado el item del menu enviado como parametro?
	 */
	$scope.isSelectedItem = function(itemId){
		return (selectedItemId == itemId);
	}
	
	/**
	 * Esta seleccionado el item del submenu enviado como parametro?
	 */
	$scope.isSelectedSubmenuItem = function(itemId){
		return (selectedSubmenuItemId == itemId);
	}

	
	//items del menu principal (se define en esta instancia para cargar los metodos correctamente)
	$scope.items = [
		{id: "data", label:'Mis datos', img:'fa-pencil-square-o', function: editProfile },
		{id: "password",label:'Cambiar clave', img:'fa-lock', url:'changePassword', function: defaultActionMenu },
		{id: "user", label:'Editar usuarios', img:'fa-users', url:'editUsers', function: showSubmenuUser },
		{id: "account", label:'Pedidos de cuentas', img:'fa-inbox', url:'accountRequestEdit', function: showSubmenuAccount },
		{id: "logout", label:'Salir', img:'fa-sign-out', url:'logout', function: defaultActionMenu}
	];

	$scope.$on('UserSelectedEvent', function(event,userId) {
		editProfile();
		$rootScope.userId = userId;
	});
	
	$scope.$on('AccountRequestSelection', function(event,accountRequest) {
		$rootScope.accountRequest = accountRequest;
		defaultActionMenu();
		
	});


});

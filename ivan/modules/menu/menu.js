	
var app = angular.module('mainApp');

app.controller('MenuCtrl', function($scope, $location, Session, Utils) {
	
	$scope.session = Session.getCurrentSession();
	
	if($scope.session == null){
		$location.path('/logout');
	}
	
	$scope.selectedItemId = null; //id del item del menu seleccionado
	$scope.menuItemActive = null; //item  del menu activo
	
	$scope.submenuMain = false; //flag para indicar la visualizacion del submenu principal
	$scope.submenuUser = false; //flag para indicar la visualizacion del submenu de usuarios
	$scope.submenuAccount = false; //flag para indicar la visualizacion del submenu de cuentas
	
	$scope.selectedSubmenuItemId = null; //id del item del submenu seleccionado
	$scope.submenuItemActive = null; //item activo del submenu
	
	//inicializar items del submenu principal
	$scope.submenuItems = []; 
	$scope.items = [];
	
	
	var initializeAllSubmenu = function(){
		initializeSubmenuMain();
		initializeSubmenuUser();
		initializeSubmenuAccount();
	};
	
	var showSubmenuMain = function(){
		$scope.submenuMain = true;
	};
	
	var showSubmenuUser = function(){
		$scope.submenuUser = true;
	};
	
	var showSubmenuAccount = function(){
		$scope.submenuAccount = true;
	};
	
	
	/**
	 * Inicializar submenu
	 */
	var initializeSubmenuMain = function(){
		$scope.selectedSubmenuItemId = null;
		$scope.submenuItemActive = null;
		$scope.submenuMain = false;
	};
	
	var initializeSubmenuUser = function(){
		$scope.submenuUser = false;
		$scope.session.selectedUser = null;
		Session.saveSession($scope.session);
	};
	
	var initializeSubmenuAccount = function(){
		$scope.submenuAccount = false;
		$scope.session.accountRequest = null;
		Session.saveSession($scope.session);
	};
	
	/**
	 * Esta activo el submenu principal?
	 */
	$scope.isSubmenuMain = function(){
		return $scope.submenuMain;
	};
	 
	/**
	 * Esta activo el submenu de usuarios?
	 */
	$scope.isSubmenuUser = function(){
		return $scope.submenuUser;
	};
	 
	 /**
	 * Esta activo el submenu de cuentas?
	 */
	 $scope.isSubmenuAccount = function(){
		return $scope.submenuAccount;
	 };

	/**
	 * Seleccionar item del menu principal
	 */
	$scope.selectItem = function (itemId){
		//inicializar variables del menu
		$scope.selectedItemId = itemId;

		//inicializar submenus
		initializeAllSubmenu();
		
		//inicializar interface de visualizacion
		$location.url("");
		
		//buscar item seleccionado
		$scope.menuItemActive = Utils.filter(function(element) {
			return element.id == itemId;
		}, $scope.items)[0];
		
		//ejecutar funcion del item seleccionado
		$scope.menuItemActive.function();
	};
	
	
	/**
	 * Seleccionar item del submenu principal
	 */
	$scope.selectSubmenuItem = function(itemId){
		//inicializar variables del menu
		$scope.selectedSubmenuItemId = itemId;
		
		//inicializar interface de visualizacion
		$location.url("");
		
		//buscar item seleccionado
		$scope.submenuItemActive = Utils.filter(function(element) {
			return element.id == itemId;
		}, $scope.submenuItems)[0];
		
		//ejecutar funcion del item seleccionado
		$scope.submenuItemActive.function();
	};
	
	/**
	 * Accion por defecto del submenu
	 */
	var defaultActionMenu = function(){
		initializeAllSubmenu();
		if($scope.menuItemActive.url != undefined){
			$location.url($scope.menuItemActive.url);
		}
	};
	
	
	/**
	 * Accion por defecto del submenu
	 */
	var defaultActionSubmenu = function(){
		if($scope.submenuItemActive.url != undefined){
			$location.url($scope.submenuItemActive.url);
		}
	};
	
	var setSubmenuItemsUser = function(param) {

		$scope.submenuItems = [
			{id:'user', label:'Perfil', img:'fa-user', url:'editUserProfile/'+param, function: defaultActionSubmenu },
			{id:'student', label:'Datos de Alumno', img:'fa-university/'+param, url:'editStudent', function: defaultActionSubmenu },
			{id:'au24', label:'Au24', img:'fa-th-large', url:'#/'+param, function: defaultActionSubmenu },
			{id:'job', label:'Inserción Laboral', img:'fa-th-large/'+param, url:'#', function: defaultActionSubmenu }
		];
	};
	
	
	/**
	 * Esta seleccionado el item del menu enviado como parametro?
	 */
	$scope.isSelectedItem = function(itemId){
		return ($scope.selectedItemId == itemId);
	};
	
	/**
	 * Esta seleccionado el item del submenu enviado como parametro?
	 */
	$scope.isSelectedSubmenuItem = function(itemId){
		return ($scope.selectedSubmenuItemId == itemId);
	};

	var editProfileAction = function(){
		initializeAllSubmenu();
		setSubmenuItemsUser($scope.session.user_id);
		showSubmenuMain();
	};
	
	var editUsersAction = function(){
		initializeAllSubmenu();
		showSubmenuUser();
	};
	
	var accountRequestEditAction = function(){
		initializeAllSubmenu();
		showSubmenuAccount();
	};

	$scope.$on('UserSelectedEvent', function(event,userId) {
		initializeAllSubmenu();
		setSubmenuItemsUser(userId);
		showSubmenuMain();
	});
	
	$scope.$on('AccountRequestSelection', function(event,accountRequest) {
		initializeAllSubmenu();
		console.log(accountRequest);
		$scope.session.accountRequest = accountRequest;
		Session.saveSession($scope.session);
		defaultActionMenu();
		showSubmenuAccount();
	});



	//definir items del menu principal (se define en esta instancia para cargar los metodos correctamente)
	if($scope.session != null){
		$scope.items = [
			{id: "data", label:'Mis datos', img:'fa-pencil-square-o', function: editProfileAction },
			{id: "password",label:'Cambiar clave', img:'fa-lock', url:'changePassword', function: defaultActionMenu },
			{id: "user", label:'Editar usuarios', img:'fa-users', url:'editUsers', function: editUsersAction },
			{id: "account", label:'Pedidos de cuentas', img:'fa-inbox', url:'accountRequestEdit', function: accountRequestEditAction },
			{id: "logout", label:'Salir', img:'fa-sign-out', url:'logout', function: defaultActionMenu}
		];
	};
});
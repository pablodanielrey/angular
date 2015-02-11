

var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, $location, Session) {

  $scope.secondItems = [];
  $scope.itemSelected = null;
  $scope.selectedItemIndex = null;

	/**
   * Cargar indice del elemento seleccionado
   */
  $scope.itemClicked = function ($index) {
    $scope.selectedItemIndex = $index;
  };
  
  $scope.defaultAction = function() {
    $scope.secondItems = [];
    $scope.itemSelected = null;
    var item = $scope.items[$scope.selectedItemIndex];
    if(item.url != undefined){
	    $location.url(item.url);
	}
  }

  $scope.editProfile = function() {
    $scope.secondItems = [
    {label:'Perfil', img:'fa-user', url:'#/editUserProfile', function: $scope.editProfile },
    {label:'Datos de Alumno', img:'fa-university', url:'#/editStudent', function: $scope.editProfile },
    {label:'Au24', img:'fa-th-large', url:'#', function: $scope.editProfile },
    {label:'Inserción Laboral', img:'fa-th-large', url:'#', function: $scope.editProfile }
    ];

    $scope.itemSelected = 'editUserProfile';
  }


  $scope.items = [
{label:'Mis datos', img:'fa-pencil-square-o', function: $scope.editProfile },
{label:'Cambiar clave', img:'fa-lock', url:'changePassword', function: $scope.defaultAction },
{label:'Editar usuarios', img:'fa-users', url:'editUsers', function: $scope.defaultAction },
{label:'Pedidos de cuentas', img:'fa-inbox', url:'listAccountRequests', function: $scope.defaultAction },
{label:'Salir', img:'fa-sign-out', url:'logout', function: $scope.defaultAction }


];


/*
  $scope.items = [
{label:'Estado del sistema', url:'#/status', function: $scope.defaultAction },
{label:'Editar Usuarios', url:'#/editUsers', function: $scope.defaultAction },
{label:'Editar Grupos', url:'#/editGroups', function: $scope.defaultAction },
{label:'Editar Perfil', url:'#/editUserProfile', function: $scope.editProfile },
{label:'Listar pedidos de cuentas', url:'#/listAccountRequests', function: $scope.defaultAction },
{label:'Cambiar clave', url:'#/changePassword', function: $scope.defaultAction },
{label:'Salir', url:'#/logout', function: $scope.defaultAction }
  ];
*/



  $scope.ejemplo1 = function() {
    alert('ej1');
  }


  $scope.isSecondVisible = function() {
    return ($scope.itemSelected != null);
  }

});

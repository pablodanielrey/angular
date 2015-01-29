

var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, $location, Session) {

  $scope.secondItems = [];
  $scope.itemSelected = null;

  $scope.defaultAction = function() {
    $scope.secondItems = [];
    $scope.itemSelected = null;
  }

  $scope.editProfile = function() {
    $scope.secondItems = [
    {label:'Perfil', url:'#/editUserProfile', function: $scope.editProfile },
    {label:'Datos de Alumno', url:'#/editStudent', function: $scope.editProfile },
    {label:'Au24', url:'#', function: $scope.editProfile },
    {label:'Inserción Laboral', url:'#', function: $scope.editProfile }
    ];

    $scope.itemSelected = 'editUserProfile';
  }


  $scope.items = [
{label:'Mis datos', function: $scope.editProfile },
{label:'Cambiar clave', url:'#/changePassword', function: $scope.defaultAction },
{label:'Salir', url:'#/logout', function: $scope.defaultAction },
{label:'Listar pedidos de cuentas', url:'#/listAccountRequests', function: $scope.defaultAction },
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

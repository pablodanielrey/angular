
var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, Session) {

  $scope.items = [
{url:'#/main',label:'Principal'},
{url:'#/status',label:'Estado del sistema'},
{url:'#/editUsers',label:'Editar Usuarios'},
{url:'#/editUserProfile',label:'Editar Perfil'},
{url:'#/createAccountRequest',label:'Pedir una cuenta nueva'},
{url:'#/listAccountRequests',label:'Listar pedidos de cuentas'},
{url:'#/changePassword',label:'Cambiar clave'},
{url:'#/logout',label:'Salir'}
  ];


  $scope.isMenuVisible = function() {
    return Session.isLogged();
  }

  $rootScope.$on('loginOk', function(event,data) {

  });

  $rootScope.$on('logoutOk', function(event,data) {

  });


});

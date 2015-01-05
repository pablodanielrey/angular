
var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, Session) {

  $scope.items = [
{url:'#/main',label:'Principal'},
{url:'#/status',label:'Estado del sistema'},
{url:'#/editUsers',label:'Editar Usuarios'},
{url:'#/editProfile',label:'Editar Perfil'},
{url:'#/createAccountRequest',label:'Pedir una cuenta nueva'},
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

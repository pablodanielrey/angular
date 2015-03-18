var app = angular.module('mainApp');

app.controller('MyDataOptionCtrl', function($scope, $rootScope, Profiles, $location, Session) {

  $scope.visible = false;

  $scope.isVisible = function() {
    return $scope.visible;
  }

  $scope.$on('MenuOptionSelectedEvent', function(event,data) {
    $scope.visible = false;
    if (data == 'MyDataOption') {
      $scope.visible = true;
      $scope.itemSelected = null;

      $scope.generateItems();
    }
  });

  $scope.myProfile = function() {
    $location.path('/editUsers');
  }

  $scope.studentData = function() {
    $location.path('/editStudent');
  }

  $scope.au24 = function() {
	   $location.path('/au24');
  }

  $scope.laboralInsertion = function() {
    $location.path('/editInsertion');
  }

  $scope.systemData = function() {
    $location.path('/editSystems');
  }

  $scope.items = [];


  // se generan por los distintos perfiles de usuario
  $scope.generateItems = function() {
    Profiles.checkAccess(Session.getSessionId(),'ADMIN', function(ok) {

      if (ok == 'granted') {
        $scope.items = [];
        $scope.items.push({ label:'Perfil', img:'fa-user', url:'editUserProfile', function: $scope.myProfile });
        $scope.items.push({ label:'Datos de Alumno', img:'fa-university', url:'editStudent', function: $scope.studentData });
        $scope.items.push({ label:'Sistemas', img:'fa-user', url:'editSystems', function: $scope.systemData });
        //{ label:'Au24', img:'fa-th-large', url:'#', function: $scope.au24 }
        $scope.items.push({ label:'Inserción Laboral', img:'fa-th-large', url:'editInsertion', function: $scope.laboralInsertion });

        // selecciono por defecto el primer item.
        $scope.selectItem($scope.items[0]);
      } else {
        $scope.items = [];
        $scope.items.push({ label:'Perfil', img:'fa-user', url:'editUserProfile', function: $scope.myProfile });
        $scope.items.push({ label:'Datos de Alumno', img:'fa-university', url:'editStudent', function: $scope.studentData });
        //{ label:'Au24', img:'fa-th-large', url:'#', function: $scope.au24 }
        //{ label:'Inserción Laboral', img:'fa-th-large', url:'editInsercion', function: $scope.laboralInsertion }

        // selecciono por defecto el primer item.
        $scope.selectItem($scope.items[0]);
      }
    },
    function(error){
      alert(error);
    });
  }

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

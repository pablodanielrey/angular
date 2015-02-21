var app = angular.module('mainApp');

app.controller('MyProfileOptionCtrl', function($scope, $rootScope) {

  $scope.visible = false;

  $scope.isVisible = function() {
    return $scope.visible;
  }

  $scope.$on('MenuOptionSelectedEvent', function(event,data) {
    $scope.visible = false;
    if (data == 'MyProfileOption') {
      $scope.visible = true;
    }
  });


  $scope.myProfile = function() {

  }

  $scope.studentData = function() {

  }

  $scope.au24 = function() {

  }

  $scope.laboralInsertion = function() {

  }

  $scope.items = [
    { label:'Perfil', img:'fa-user', url:'editUserProfile', function: $scope.myProfile },
    { label:'Datos de Alumno', img:'fa-university', url:'editStudent', function: $scope.studentData },
    { label:'Au24', img:'fa-th-large', url:'#', function: $scope.au24 },
    { label:'Inserción Laboral', img:'fa-th-large', url:'editInsercion', function: $scope.laboralInsertion }
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

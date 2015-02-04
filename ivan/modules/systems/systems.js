
var app = angular.module('mainApp');


app.controller('SystemsCtrl', function($scope) {

  $scope.systems = [
    {name:'Estudiante', url:'#/editStudent'},
    {name:'Au24', url:'#/au24'}
  ];


});

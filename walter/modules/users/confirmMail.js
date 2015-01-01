
var app = angular.module('mainApp');


app.controller('ConfirmMailCtrl',function($scope,$routeParams,Users) {

  $scope.message = '';

  if ($routeParams['hash'] == undefined) {
    $scope.message = 'no se ha definido el mail a confirmar';
    return;
  }

  var hash = $routeParams['hash'];
  Users.confirmMail(hash,
    function(ok) {
      $scope.message = 'Requerimiento procesado correctamente';
    },
    function(error) {
      alert(error);
  });

});

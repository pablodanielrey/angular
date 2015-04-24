
var app = angular.module('mainApp');


app.controller('ConfirmMailCtrl',function($scope,$routeParams,Users,$timeout,Notifications,$window) {

  $scope.message = '';

  if ($routeParams['hash'] == undefined) {
    $scope.message = 'no se ha definido el mail a confirmar';
    return;
  }

  var hash = $routeParams['hash'];
  Users.confirmMail(hash,
    function(ok) {
      Notifications.message('Requerimiento procesado correctamente');
      $timeout(function() {
        $window.location.href = "/systems/login/indexLogin.html";
      }, 3000);
    },
    function(error) {
      Notificactions.message(error);
      $timeout(function() {
        $window.location.href = "/systems/login/indexLogin.html";
      }, 3000);
  });



});

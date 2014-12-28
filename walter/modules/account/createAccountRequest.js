
var app = angular.module('mainApp');


app.controller('CreateAccountRequestCtrl', function($scope, Messages, Utils, Session) {

  $scope.request = {
          name:'',
          lastname:'',
          dni:'',
          email:'',
          reason:''
  };

  $scope.createRequest = function() {

    var msg = {
        id: Utils.getId(),
        action: 'createAccountRequest',
        session: Session.getSessionId(),
        request: $scope.request
    };

    Messages.send(msg, function(response) {

      alert('Pedido de cuenta creado correctamente, se confirmará mediante un mail a su dirección de correo');

    });

    clearRequest();
  };

  clearRequest = function() {
    $scope.request.name = '';
    $scope.request.lastname = '';
    $scope.request.dni = '';
    $scope.request.email = '';
    $scope.request.reason = '';
  }

});

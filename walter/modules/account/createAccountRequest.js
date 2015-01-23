
var app = angular.module('mainApp');


app.controller('CreateAccountRequestCtrl', function($scope, Messages, Utils, Session) {

  $scope.request = {
          name:'',
          lastname:'',
          dni:'',
          email:'',
          reason:'',
          password:'',
          password2:''
  };

  $scope.createRequest = function() {

    if ($scope.request.password != $scope.request.password2) {
      alert('las claves ingresadas no son iguales');
      $scope.request.password = '';
      $scope.request.password2 = '';
      return;
    }


    var msg = {
        id: Utils.getId(),
        action: 'createAccountRequest',
        session: Session.getSessionId(),
        request: $scope.request
    };

    Messages.send(msg, function(response) {

      if (response.ok == undefined) {
        alert('error creando el pedido');
      } else {
        alert('Pedido de cuenta creado correctamente, se confirmará mediante un mail a su dirección de correo');
      }


    });

    clearRequest();
  };

  clearRequest = function() {
    $scope.request = {
      name:'',
      lastname:'',
      dni:'',
      email:'',
      reason:'',
      password:'',
      password2:''
    };
  }

});

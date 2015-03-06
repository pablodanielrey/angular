
var app = angular.module('mainApp');


app.controller('CreateAccountRequestCtrl', function($rootScope, $scope, $window, $timeout, Messages, Utils, Session) {
  $scope.request = { };


	/**
	 * Verificar variables y en caso afirmativo enviar mensaje de requirimiento de creacion de cuenta
	 */
	$scope.createRequest = function() {

    var createForm = document.getElementById('createForm');
    if (!createForm.checkValidity()) {
      return;
    }

		if ($scope.request.password != $scope.request.password2) {
      $rootScope.$broadcast('ShowMessageEvent',['Las claves ingresadas no son iguales','Ingrese nuevamente la información de la clave']);
//			alert('las claves ingresadas no son iguales');
			$scope.request.password = '';
			$scope.request.password2 = '';
			return;
		}


    if ($scope.request.reason == '') {
      $rootScope.$broadcast('ShowMessageEvent',['Debe seleccionar un motivo para crear la cuenta']);
      return
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
				$window.location.href = "/#/main"
			}

		});

		$scope.clearRequest();
	};

  $scope.clearRequest = function() {
      $scope.request = { };
  };


  $timeout(function() {
    $scope.clearRequest();
  },0)

});

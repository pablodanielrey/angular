
var app = angular.module('mainApp');

app.controller('ConnectionCtrl', function($scope, WebSocket, Session) {

  $scope.connected = false;

$scope.displayLog = "{color:'red'}";

  $scope.$on('onSocketOpened', function(event,data) {
    $scope.connected = true;
  });

  $scope.$on('onSocketClosed', function(event,data) {
    $scope.connected = false;
  });

  $scope.isConnected = function() {
    return $scope.connected;
  };
  
	/**
	 * Obtener nombre de usuario conectado
	 * @returns {Session@call;getCurrentSession.login.username}
	 */
	$scope.getConnectedUserName = function(){
		var user = Session.getCurrentSession();

		return user.login.username;
	};

	$scope.connect = function() {
		WebSocket.registerHandlers();
	};

});

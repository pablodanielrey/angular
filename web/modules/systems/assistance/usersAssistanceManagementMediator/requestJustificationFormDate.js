
app.controller('UsersAssistanceManagementMediatorRequestJustificationFormDateCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");
  
  //***** variables del formulario de solicitud *****
  $scope.model.date = null;

  
  
  /******************
   * INICIALIZACION *
   ******************/
  $scope.clearForm = function(){
    $scope.model.date = null;
  };
  

  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, data){
    $scope.clearForm();

	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
    $scope.clearForm();
	});
  
  
  $scope.$watch('model.selectedUser', function() {
      $scope.clearForm();
  }); 
  
  $scope.$watch('model.justificationSelectedId', function() {
    $scope.clearForm();
  });
  

}]);

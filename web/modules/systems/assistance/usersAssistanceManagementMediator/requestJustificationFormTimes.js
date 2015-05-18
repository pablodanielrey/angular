
app.controller('UsersAssistanceManagementMediatorRequestJustificationFormTimesCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");
  
  //***** variables del formulario de solicitud *****
  $scope.model.date = null; 
  $scope.model.begin = null;
  $scope.model.end = null; 

  
  
  /******************
   * INICIALIZACION *
   ******************/
  $scope.clearForm = function(){
      $scope.model.date = null; 
    $scope.model.begin = null; 
    $scope.model.end = null; 
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
  
  
  
  $scope.checkTimes = function(){
    if($scope.model.end !== null){
      if(($scope.model.begin !== null) && ($scope.model.begin > $scope.model.end)){
        $scope.model.end = new Date($scope.model.begin);
      }
    }
  };



}]);

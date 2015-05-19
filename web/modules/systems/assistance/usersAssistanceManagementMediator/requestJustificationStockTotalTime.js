
app.controller('UsersAssistanceManagementMediatorRequestJustificationStockTotalTimeCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");
  
  //***** variables de la visualizacion de stock *****
  $scope.justification.stock = null;
  
  
  
  
  
  
  
  /******************
   * INICIALIZACION *
   ******************/
  $scope.clearStock = function(){
    $scope.justification.stock = null;
  };
  
  


  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, data){
    if ($scope.model.selectedUser.id === data.user_id) {
      $scope.clearStock();
      $scope.loadStockTotalTime();
    }
	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
    for (var i = 0; i < $scope.model.requestedJustificationsFiltered.length; i++) {
      if ($scope.model.requestedJustificationsFiltered[i].id === data.request_id) {
        $scope.clearStock();
        $scope.loadStockTotalTime();
      }
    }
	});
  
  
  
  $scope.$watch('model.selectedUser', function() {
    $scope.clearStock();
    if($scope.model.selectedUser){
      $scope.loadStockTotalTime();
    }
  }); 
  
 
  

  


}]);

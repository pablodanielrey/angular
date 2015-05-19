
app.controller('UsersAssistanceManagementMediatorRequestJustificationFormDateConfirmationCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");
  
  //***** variables del formulario de solicitud *****
  $scope.model.date = null; //definida en controlador hermano
  $scope.model.dateFormated = null;
  $scope.model.processingRequest = false;


  
  
  /******************
   * INICIALIZACION *
   ******************/
  $scope.clearConfirmation = function(){
    $scope.model.dateFormated = null;
    $scope.model.processingRequest = false;
  };
  

  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, data){
    $scope.clearConfirmation();

	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
    $scope.clearConfirmation();
	});
  
  
  $scope.$watch('model.selectedUser', function() {
      $scope.clearConfirmation();
  }); 
  
  $scope.$watch('model.justificationSelectedId', function() {
    $scope.clearConfirmation();
  });
  
  
  $scope.$watch('model.date', function() {
    $scope.model.dateFormated = null;
    if($scope.model.date !== null){
			$scope.model.dateFormated = Utils.formatDate($scope.model.date);
    }
  }); 
  
  $scope.isDateDefined = function(){
    return ($scope.model.dateFormated !== null);    
  };
  
  
 $scope.save = function() {
   
   $scope.model.processingRequest = true;
    var request = {
			id:$scope.justification.id,
			begin:$scope.model.date,
		};
    
    
    console.log($scope.model.selectedUser);
    console.log(request);
    

    Assistance.requestJustification($scope.model.selectedUser.id, request, 'APPROVED',
			function(ok) {
				$scope.clearConfirmation(); //limpiar contenido
        $scope.clearSections();
        $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
        Notifications.message("Solicitud de " + $scope.justification.name + " registrada correctamente");
			},
			function(error){
        $scope.clearConfirmation();    //limpiar contenido
        $scope.clearSections();
        $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
				Notifications.message(error);
			}
		);
  };
  
  




}]);

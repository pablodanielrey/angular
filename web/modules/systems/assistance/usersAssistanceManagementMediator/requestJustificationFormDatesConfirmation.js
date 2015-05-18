
app.controller('UsersAssistanceManagementMediatorRequestJustificationFormDatesConfirmationCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");
  
  //***** variables del formulario *****  
  $scope.model.begin = null; //definida en controlador hermano
  $scope.model.end = null; //definida en controlador hermano
  $scope.model.beginFormated = null; //fecha en formato amigable para el usuario
  $scope.model.endFormated = null; //fecha en formato amigable para el 

  
  
  /******************
   * INICIALIZACION *
   ******************/
  $scope.clearConfirmation = function(){
    $scope.model.beginFormated = null;
    $scope.model.endFormated = null;
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
  
  
  $scope.$watch('model.begin', function() {
    $scope.model.beginFormated = null;
    if($scope.model.begin !== null){
			$scope.model.beginFormated = Utils.formatDate($scope.model.begin);
    }
  }); 
  
  $scope.$watch('model.end', function() {
    $scope.model.endFormated = null;
    if($scope.model.end !== null){
			$scope.model.endFormated = Utils.formatDate($scope.model.end);
    }
  });
  
  $scope.isDatesDefined = function(){
    return ($scope.model.beginFormated !== null && $scope.model.endFormated !== null);    
  };
  
  
 $scope.save = function() {
   
   $scope.model.processingRequest = true;
    var request = {
			id:$scope.justification.id,
			begin:$scope.model.begin,
      end:$scope.model.end,
      status:"APPROVED"
		};    

    Assistance.requestJustificationRange($scope.model.selectedUser.id, request,
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


app.controller('UsersAssistanceManagementMediatorRequestJustificationFormTimesConfirmationCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");
  
  //***** variables del formulario *****  
  $scope.model.date = null; //definida en controlador hermano
  $scope.model.begin = null; //definida en controlador hermano
  $scope.model.end = null; //definida en controlador hermano
  $scope.model.dateFormated = null; //fecha en formato amigable para el usuario
  $scope.model.beginTimeFormated = null; //fecha en formato amigable para el usuario
  $scope.model.timeFormated = null; //diferencia de tiempo en formato amigable para el usuario
  $scope.model.endTimeFormated = null; //fecha en formato amigable para el 
  
  $scope.model.processingRequest = false;

  
  
  /******************
   * INICIALIZACION *
   ******************/
  $scope.clearConfirmation = function(){
    $scope.model.beginTimeFormated = null;
    $scope.model.endTimeFormated = null;
    $scope.model.timeFormated = null;
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
  
  $scope.$watch('model.begin', function() {
    $scope.model.beginTimeFormated = null;
    if($scope.model.begin !== null){
			$scope.model.beginTimeFormated = Utils.formatTime($scope.model.begin);
    }
    $scope.defineTimeFormated();
  });
  
  $scope.$watch('model.end', function() {
    $scope.model.endTimeFormated = null;
    if($scope.model.end !== null){
			$scope.model.endTimeFormated = Utils.formatTime($scope.model.end);
    }
    $scope.defineTimeFormated();
  });
  
  $scope.defineTimeFormated = function(){
    if ($scope.model.begin && $scope.model.end) $scope.model.timeFormated = Utils.getDifferenceTimeFromDates($scope.model.begin, $scope.model.end);
  }
  
  $scope.isDatesDefined = function(){
    return ($scope.model.beginTimeFormated !== null && $scope.model.endTimeFormated !== null && $scope.model.dateFormated !== null);    
  };
  
  
 $scope.save = function() {
   
   $scope.model.processingRequest = true;
   
    var request = {
			id:$scope.justification.id,
			begin:new Date($scope.model.date),
      end:new Date($scope.model.date),
      status:"APPROVED"
		};    
    
    request.begin.setHours($scope.model.begin.getHours(), $scope.model.begin.getMinutes());
    request.end.setHours($scope.model.end.getHours(), $scope.model.end.getMinutes());

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

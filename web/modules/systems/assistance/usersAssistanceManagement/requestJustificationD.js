
app.controller('UsersAssistanceManagementRequestJustificationDCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");
  

  $scope.rjModel = {
    id: '0cd276aa-6d6b-4752-abe5-9258dbfd6f09',
    name: Utils.getJustificationName('0cd276aa-6d6b-4752-abe5-9258dbfd6f09'),
    section: null,
      
    begin: null,
    beginFormated: null,
    end: null,
    endFormated: null,
    processingRequest: null,

  };
  
  
  


  
  /******************
   * INICIALIZACION *
   ******************/
  $scope.clear = function(){
    $scope.rjModel.begin = null;
    $scope.rjModel.beginFormated = null;
    $scope.rjModel.end = null;
    $scope.rjModel.endFormated = null;
    $scope.rjModel.processingRequest = false;
    $scope.rjModel.section = null;

  };
  

  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, data){
    $scope.model.justificationSelectedId = null;
    $scope.clear();
	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
    $scope.model.justificationSelectedId = null;
    $scope.clear();
	});
  
  
  $scope.$watch('model.selectedUser', function() {
    $scope.model.justificationSelectedId = null;
    $scope.clear();
  }); 
  
  $scope.$watch('model.justificationSelectedId', function() {
    $scope.clear();
  });
  
  


  //***** METODOS DE SELECCION DE LA SECCION *****
  /**
   * Esta seleccionada la seccion correspondiente a la justificacion?
   * @returns {Boolean}
   */
  $scope.isSelectedJustification = function() {
    return ($scope.model.justificationSelectedId === $scope.rjModel.id);
  };


  /**
   * Modificar seleccion de opcion desplegable correspondiente a salidas eventuales
   * @returns {Boolean}
   */
	$scope.selectJustification = function() {
    if($scope.model.selectedUser === null){
      $scope.model.justificationSelectedId = null;
      Notifications.message("Debe seleccionar usuario");
      return;
    }
    if($scope.model.justificationSelectedId === $scope.rjModel.id){
      $scope.model.justificationSelectedId = null;
    } else {
      $scope.model.justificationSelectedId = $scope.rjModel.id;
    }
	};
  

 
  
  
  /********
   * DATE *
   ********/
  
  
  $scope.isDataDefined = function(){
    return (($scope.rjModel.begin !== null) && ($scope.rjModel.end !== null));    
  };
  
  $scope.selectDate = function(){
    if($scope.rjModel.end !== null){
      if(($scope.rjModel.begin !== null) && ($scope.rjModel.begin > $scope.rjModel.end)){
        $scope.rjModel.end = new Date($scope.rjModel.begin);
      }
    }
    
    $scope.rjModel.beginFormated = null;
    if($scope.rjModel.begin !== null){
			$scope.rjModel.beginFormated = Utils.formatDate($scope.rjModel.begin);
    }
    
    $scope.rjModel.endFormated = null;
    if($scope.rjModel.end !== null){
			$scope.rjModel.endFormated = Utils.formatDate($scope.rjModel.end);
    }
  };

  
  
  
  $scope.save = function() {
   
   $scope.rjModel.processingRequest = true;
   
    var request = {
			id:$scope.rjModel.id,
			begin:$scope.rjModel.begin,
      end:$scope.rjModel.end,
		};

    Assistance.requestJustificationRange($scope.model.selectedUser.id, request, 'APPROVED',
			function(ok) {
				$scope.clear(); //limpiar contenido
        $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
        Notifications.message("Solicitud de " + $scope.rjModel.name + " registrada correctamente");
			},
			function(error){
        $scope.clear();    //limpiar contenido
        $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
				Notifications.message(error);
			}
		);
  };
  
  
}]);

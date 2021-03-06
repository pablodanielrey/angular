
app.controller('UsersAssistanceManagementRequestJustificationICCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");
  

  $scope.rjModel = {
    id: '3d486aa0-745a-4914-a46d-bc559853d367',
    name: Utils.getJustificationName('3d486aa0-745a-4914-a46d-bc559853d367'),
    section: null,
      
    date: null,
    dateFormated: null,
    processingRequest: null,
    
    stock: null,
    stockYear: null
  };
  
  
  


  
  /******************
   * INICIALIZACION *
   ******************/
  $scope.clear = function(){
    $scope.rjModel.date = null;
    $scope.rjModel.dateFormated = null;
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
    return ($scope.rjModel.date !== null);    
  };
  
  $scope.defineData = function() {
    $scope.rjModel.dateFormated = null;
    if($scope.rjModel.date !== null){
			$scope.rjModel.dateFormated = Utils.formatDate($scope.rjModel.date);
    }
  }; 
  
  
  
  $scope.save = function() {
   
   $scope.rjModel.processingRequest = true;
   
    var request = {
			id:$scope.rjModel.id,
			begin:$scope.rjModel.date,
		};

    Assistance.requestJustification($scope.model.selectedUser.id, request, 'APPROVED',
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

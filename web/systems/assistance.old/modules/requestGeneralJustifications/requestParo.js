
app.controller('RequestParoCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");
  

  $scope.rjModel = {
    id: '874099dc-42a2-4941-a2e1-17398ba046fc',
    name: Utils.getJustificationName('874099dc-42a2-4941-a2e1-17398ba046fc'),
      
    date: null,
    dateFormated: null,
    processingRequest: null
  };
  

  /******************
   * INICIALIZACION *
   ******************/
  $scope.clear = function(){
    $scope.rjModel.date = null;
    $scope.rjModel.dateFormated = null;
    $scope.rjModel.processingRequest = false;
  };
  

  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, data){
    $scope.model.justificationSelectedId = null;
    $scope.clear();

	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
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
    if($scope.model.justificationSelectedId === $scope.rjModel.id){
      $scope.model.justificationSelectedId = null;
    } else {
      $scope.model.justificationSelectedId = $scope.rjModel.id;
    }
	};
  

  /********
   * DATA *
   ********/
  $scope.isDataDefined = function(){
    return ($scope.rjModel.date !== null);    
  };
  
  $scope.selectData = function() {
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
    
    Assistance.requestGeneralJustification(request,
			function(ok) {
				$scope.clear(); //limpiar contenido
        $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
        Notifications.message("Solicitud de " + $scope.rjModel.name + " registrada correctamente");
	  		$scope.loadRequestedJustifications();
			},
			function(error){
        $scope.clear();    //limpiar contenido
        $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
				Notifications.message(error);
			}
		);
  };

}]);

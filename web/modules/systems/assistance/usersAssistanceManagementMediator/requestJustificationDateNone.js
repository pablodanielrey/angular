
app.controller('UsersAssistanceManagementMediatorRequestJustificationDateNoneCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");

  //***** variables de seleccion de la seccion *****
  $scope.model.requestSelected = false; //flag para indicar la seleccion del formulario de solicitud
  
  //***** variables del formulario de solicitud *****
  $scope.model.date = null;
  $scope.model.dateFormated = null;
  $scope.model.processingRequest = false;  //flag para indicar que se esta procesando el formulario de solicitud


  
  
  
  /******************
   * INICIALIZACION *
   ******************/
  $scope.clearContent = function(){
    $scope.model.requestSelected = false;
    $scope.model.date = null;
    $scope.model.dateFormated = null;
    $scope.model.processingRequest = false;
  };
  

  
  
  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, data){
    if ($scope.model.selectedUser.id === data.user_id) {
      $scope.clearContent();
      $scope.loadRequestedJustifications();
      $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
    }
	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
    for (var i = 0; i < $scope.model.requestedJustificationsFiltered.length; i++) {
      if ($scope.model.requestedJustificationsFiltered[i].id === data.request_id) {
        $scope.clearContent();
        $scope.loadRequestedJustifications();
        $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
      }
    }
	});
    
    
  $scope.$watch('model.selectedUser', function() {
    if($scope.model.selectedUser){
       $scope.clearContent();
    } else {
      $scope.clearContent();
      $scope.model.justificationSelectedId = null;
    }
  }); 
  
  $scope.$watch('model.justificationSelectedId', function() {
    $scope.clearContent();
  });
  
  

  
  
  
  /*************************************
   * METODOS DE SELECCION DE SECCIONES *
   *************************************/
  /**
   * Esta seleccionado el formulario para solicitar justificaicion?
   * @returns {Boolean}
   */
	$scope.isSelectedRequest = function() {
		return $scope.model.requestSelected;
	};

  
  /**
   * Seleccionar formulario para definir una solicitud del articulo 102
   * @returns {Boolean}
   */
	$scope.selectRequest = function() {
  	$scope.clearContent();
		$scope.model.requestSelected = true;
	};




  /**************************************
   * DEFINICION DE DATOS DEL FORMULARIO *
   **************************************/
  $scope.isDateDefined = function(){
    return ($scope.model.date !== null);    
  };
  
  $scope.selectDate = function(){
		$scope.model.dateFormated = null;
    if($scope.model.date !== null){
			$scope.model.dateFormated = Utils.formatDate($scope.model.date);
    }
  };
  
  $scope.save = function() {
   
   $scope.model.processingRequest = true;
    var request = {
			id:$scope.justification.id,
			begin:$scope.model.date,
      status:"APPROVED"
		};

    Assistance.requestJustification($scope.model.selectedUser.id, request,
			function(ok) {
				$scope.clearContent();    //limpiar contenido
        $scope.model.processingRequest = false; //habilitar formulario
        $scope.model.justificationSelectedId = null;
        Notifications.message("Solicitud de " + $scope.justification.name + " registrada correctamente");
			},
			function(error){
				Notifications.message(error);
			}

		);

  };
  
  
 
  
  
  
  
 
  



}]);

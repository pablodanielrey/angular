
app.controller('UsersAssistanceManagementMediatorRequestJustificationDateTotalCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");

  //***** variables de seleccion de la seccion *****
  $scope.model.requestSelected = false; //flag para indicar la seleccion del formulario de solicitud
  $scope.model.availableSelected = false; //flag para indicar la seleccion de la visualizacion de disponibilidad
  
  //***** variables del formulario de solicitud *****
  $scope.model.date = null;
  $scope.model.dateFormated = null;
  $scope.model.processingRequest = false;  //flag para indicar que se esta procesando el formulario de solicitud

  
  
  //***** variables de la visualizacion de stock *****
  $scope.justification.stock = null;
  
  
  
  
  
  
  
  /******************
   * INICIALIZACION *
   ******************/
  $scope.clearContent = function(){
    $scope.model.availableSelected = false;
    $scope.model.requestSelected = false;
    $scope.model.date = null;
    $scope.model.dateFormated = null;
    $scope.model.processingRequest = false;
  };
  
  
  $scope.loadStock = function(){
    $scope.loadStockTotal();
  };


  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, data){
    if ($scope.model.selectedUser.id === data.user_id) {
      $scope.clearContent();
      $scope.loadRequestedJustifications();
      $scope.loadStock();
      $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
    }
	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
    for (var i = 0; i < $scope.model.requestedJustificationsFiltered.length; i++) {
      if ($scope.model.requestedJustificationsFiltered[i].id === data.request_id) {
        $scope.clearContent();
        $scope.loadRequestedJustifications();
        $scope.loadStock();
        $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
      }
    }
	});
  
  
  
  $scope.$watch('model.selectedUser', function() {
    if($scope.model.selectedUser){
      $scope.clearContent();
      $scope.loadStock();
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
   * Esta seleccionada la seccion para ver la disponibilidad?
   * @returns {Boolean}
   */
  $scope.isSelectedAvailable = function() {
		return $scope.model.availableSelected;
	};



  /**
   * Seleccionar formulario para definir una solicitud del articulo 102
   * @returns {Boolean}
   */
	$scope.selectRequest = function() {
  	$scope.clearContent();
		$scope.model.requestSelected = true;
	};


  /**
   * Seleccionar seccion para ver la disponibilidad correspondiente al articulo 102
   * @returns {Boolean}
   */
	$scope.selectAvailable = function() {
		$scope.clearContent();
		$scope.model.availableSelected = true;

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
     
				$scope.clearContent(); //limpiar contenido
        $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
        Notifications.message("Solicitud de " + $scope.justification.name + " registrada correctamente");
			},
			function(error){
        $scope.clearContent();    //limpiar contenido
        $scope.model.justificationSelectedId = null; //limpiar seleccion de justificacion
				Notifications.message(error);
			}
		);
  };
  
  
  
  
    
  
  
  
  
  
  
  

 
  



}]);

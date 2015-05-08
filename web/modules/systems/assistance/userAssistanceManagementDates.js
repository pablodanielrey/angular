var app = angular.module('mainApp');

app.controller('UserAssistanceManagementDatesCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");


  $scope.init = function(justificationId, justificationSelectedName){
    //***** inicializar datos de la justificacion *****
    $scope.justification = { 
      id: justificationId, //id de la justificacion
      name:Utils.getJustificationName(justificationId),
      stock:0,
      yearlyStock:0,
      selectedName:justificationSelectedName
    };
    
    $scope.model[justificationSelectedName] = false; //inicializar flag para indicar la seleccion de la justificacion
    
    
  };
  

  //***** variables del formulario *****  
  $scope.model.begin = null;         //fecha seleccionada
  $scope.model.beginFormated = null; //fecha en formato amigable para el usuario
  $scope.model.end = null;         //fecha seleccionada
  $scope.model.endFormated = null; //fecha en formato amigable para el usuario
  
  $scope.model.processingRequest = false;
  
  
  //***** METODOS DE SELECCION DE LA SECCION *****
  /**
   * Esta seleccionada la seccion correspondiente a la justificacion 102
   * @returns {Boolean}
   */
  $scope.isSelectedJustification = function() {
    
    return $scope.model[$scope.justification.selectedName];
  };

  /**
   * Modificar seleccion de opcion desplegable correspondiente a salidas eventuales
   * @returns {Boolean}
   */
	$scope.selectJustification = function() {
    var value = !$scope.model[$scope.justification.selectedName];
    $scope.clearSelections();
    $scope.clearContent();
    $scope.model[$scope.justification.selectedName] = value;
	};
  
  
  /**
   * Inicializar variables correspondientes al contenido de la seccion del articulo 102
   * @returns {undefined}
   */
  $scope.clearContent = function(){
    $scope.model.begin = null;
		$scope.model.beginFormated = null;
    $scope.model.processingRequest = false;
    
  };
  
    
    
  //***** METODOS DEl FORMULARIO DE SOLICITUD *****
  $scope.selectDates = function(){
		$scope.model.dateFormated = null;
    if($scope.model.date !== null){
			$scope.model.dateFormated = Utils.formatDate($scope.model.date);
    }
  };
  
  
  $scope.isDatesDefined = function(){
    return (($scope.model.begin !== null) && ($scope.model.end !== null));  
  };
  
  
  
  // Envio la peticion al servidor
  $scope.save = function() {
    $scope.model.processingRequest = true;
    var request = {
			id:$scope.justification.id,
			begin:$scope.model.begin,
      end:$scope.model.end
		};

  	Assistance.requestJustification($scope.model.session.user_id, request,
			function(ok) {
				$scope.clearContent();    //limpiar contenido
        $scope.clearSelections(); //limpiar selecciones
        Notifications.message("Solicitud de " + $scope.justification.name + " registrada correctamente");
			},
			function(error){
				Notifications.message(error);
			}

		);

  };

}]);

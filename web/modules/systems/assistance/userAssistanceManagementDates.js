var app = angular.module('mainApp');

app.controller('UserAssistanceManagementDatesCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");

  //***** datos de la justificacion *****
  $scope.justification = { 
    id: '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb', //id de la justificacion.
    name:Utils.getJustificationName('4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb'),
    stock:0,
    yearlyStock:0,
    selectedName:"justification102Selected", //Nombre de la seleccion en el controlador padre
  };
  
  //***** variables de seleccion de la seccion *****
  $scope.model.requestSelected = false; //flag para indicar la seleccion del formulario de solicitud del articulo 102
  $scope.model.availableSelected = false; //flag para indicar la seleccion de la visualizacion de disponibilidad del articulo 102
  
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

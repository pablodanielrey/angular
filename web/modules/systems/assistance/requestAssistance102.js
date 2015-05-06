var app = angular.module('mainApp');

app.controller('RequestAssistance102Ctrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {


  if(!$scope.model) $scope.model = {};
  
  //***** variables de seleccion de la seccion *****
  $scope.model.justification102Selected = false; //flag para indicar la seleccion de la seccion del articulo 102
  $scope.model.requestSelected = false; //flag para indicar la seleccion del formulario de solicitud del articulo 102
  $scope.model.availableSelected = false; //flag para indicar la seleccion de la visualizacion de disponibilidad del articulo 102
  
  
 
  
  
  //***** METODOS DE SELECCION DE LA SECCION CORRESPONDIENTE A LA JUSTIFICACION 102 *****
  /**
   * Esta seleccionada la seccion correspondiente a la justificacion 102
   * @returns {Boolean}
   */
  $scope.isSelectedJustification102 = function() {
    return $scope.model.justification102Selected;
  };

  /**
   * Modificar seleccion de opcion desplegable correspondiente a salidas eventuales
   * @returns {Boolean}
   */
	$scope.selectJustification102 = function() {
    var value = !$scope.model.justification102Selected;
    $scope.clearSelections();
    $scope.clearContent();
    $scope.model.justification102Selected = value;
	};
  
  
  /**
   * Esta seleccionado el formulario para solicitar articulo 102?
   * @returns {Boolean}
   */
	$scope.isSelectedRequest = function() {
		return $scope.model.requestSelected;
	};

  /**
   * Esta seleccionada la seccion para ver la disponibilidad del articulo 102?
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
  
  /**
   * Inicializar variables correspondientes al contenido de la seccion del articulo 102
   * @returns {undefined}
   */
  $scope.clearContent = function(){
    //Por el momento no hay variables a inicializar
    
  };
  
  
  
  
  
  //***** METODOS DE SELECCION DE LA SECCION CORRESPONDIENTE A LA JUSTIFICACION 102 *****
  
  
  
}]);

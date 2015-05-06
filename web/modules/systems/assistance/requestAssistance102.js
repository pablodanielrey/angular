var app = angular.module('mainApp');

app.controller('RequestAssistance102Ctrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");

  //***** datos de la justificacion *****
  $scope.justification = { 
    id: '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb', //id de la justificacion
    stock:0,
    yearlyStock:0
  };
  
  //***** variables de seleccion de la seccion *****
  $scope.model.justification102Selected = false; //flag para indicar la seleccion de la seccion del articulo 102
  $scope.model.requestSelected = false; //flag para indicar la seleccion del formulario de solicitud del articulo 102
  $scope.model.availableSelected = false; //flag para indicar la seleccion de la visualizacion de disponibilidad del articulo 102
  
  //***** variables del formulario *****  
  $scope.model.date = null;         //fecha seleccionada
  $scope.model.dateFormated = null; //fecha en formato amigable para el usuario
  
  
  //***** METODOS DE CARGA E INICIALIZACION *****
  /**
   * Consultar stock de la justificacion
   */
  $scope.loadStock = function(){
    Assistance.getJustificationStock($scope.model.session.user_id, $scope.justification.id, null, null,
      function(justification) {
        $scope.justification.stock = justification.stock;
      },
      function(error) {
        Notifications.message(error);
      }
    );
    Assistance.getJustificationStock($scope.model.session.user_id, $scope.justification.id, null, 'YEAR',
      function(justification) {
        $scope.justification.yearlyStock = justification.stock;
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };
  
  
  $scope.$on('findStockJustification', function(event, data) {
    if (data.justification.id == $scope.justification.id) {
        $scope.loadStock();
    }
  });

  $scope.$on('JustificationStockChangedEvent', function(event, data) {
    if ($scope.justification.id == data.justification_id) {
      $scope.loadStock();
    }
  });

  
  
  
  
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
    $scope.model.requestSelected = false;
    $scope.model.availableSelected = false;
    $scope.model.date = null;
		$scope.model.dateFormated = null;
    
  };
  
    
    
  //***** METODOS DEl FORMULARIO DE SOLICITUD DE JUSTIFICACION 102 *****
  $scope.selectDate = function(){
		$scope.model.dateFormated = null;
    if($scope.model.date !== null){
			$scope.model.dateFormated = Utils.formatDate($scope.model.date);
    }
  };
  
  
  $scope.isDateDefined = function(){
    return ($scope.model.date !== null);    
  };
  
  $scope.isStock = function(){
    return ($scope.justification.stock !== 0);
  };
  
  
  // Envio la peticion al servidor
  $scope.save = function() {
    console.log("estoy");
    var request = {
			id:$scope.justification.id,
			begin:$scope.model.date
		};

  	Assistance.requestJustification($scope.model.session.user_id, request,
			function(ok) {
				$scope.clearContent();    //limpiar contenido
        $scope.clearSelections(); //limpiar selecciones
        Notifications.message("Solicitud de artículo 102 registrada correctamente");
			},
			function(error){
				Notifications.message(error);
			}

		);

  };

}]);

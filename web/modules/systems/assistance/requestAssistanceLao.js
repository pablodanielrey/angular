var app = angular.module('mainApp');

app.controller('RequestAssistanceLaoCtrl', function($scope, Assistance, Session, Notifications, Utils) {


  if(!$scope.model) Notifications.message("No esta definido el modelo");

  //***** datos de la justificacion *****
  $scope.justification = {
    id: '76bc064a-e8bf-4aa3-9f51-a3c4483a729a', //id de la justificacion.
    name:Utils.getJustificationName('76bc064a-e8bf-4aa3-9f51-a3c4483a729a'),
    stock:0,
    yearlyStock:0,
    selectedName:"justificationLaoSelected", //Nombre de la seleccion en el controlador padre
  };


   //***** variables de seleccion de la seccion *****
  $scope.model.requestSelected = false; //flag para indicar la seleccion del formulario de solicitud del articulo 102
  $scope.model.availableSelected = false; //flag para indicar la seleccion de la visualizacion de disponibilidad del articulo 102

  //***** variables del formulario *****
  $scope.model.begin = null;         //fecha de inicio seleccionada
  $scope.model.beginFormated = null; //fecha en formato amigable para el usuario
  $scope.model.end = null;         //fecha de fin seleccionada
  $scope.model.endFormated = null; //fecha en formato amigable para el usuario

  $scope.model.processingRequest = false;




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
  };


  $scope.$on('findStockJustification', function(event, data) {
    if (data.justification.id === $scope.justification.id) {
        $scope.loadStock();
    }
  });

  $scope.$on('JustificationStockChangedEvent', function(event, data) {
    if ($scope.justification.id === data.justification_id) {
      $scope.loadStock();
    }
  });



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
    $scope.model.begin = null;
		$scope.model.beginFormated = null;
    $scope.model.end = null;
		$scope.model.endFormated = null;
    $scope.model.processingRequest = false;

  };





  //***** METODOS DEl FORMULARIO DE SOLICITUD *****
  $scope.selectDates = function(){
		$scope.model.beginFormated = null;
    $scope.model.endFormated = null;
    if($scope.model.begin !== null){
			$scope.model.beginFormated = Utils.formatDate($scope.model.begin);
    }
    if($scope.model.end !== null){
      if($scope.model.begin > $scope.model.end){
        $scope.model.end = new Date($scope.model.begin);
      }
      $scope.model.endFormated = Utils.formatDate($scope.model.end);
    }
  };


  $scope.isDatesDefined = function(){
    return (($scope.model.begin !== null) && ($scope.model.end !== null));
  };

  $scope.isStock = function(){
    return ($scope.justification.stock !== 0);
  };


  // Envio la peticion al servidor
  $scope.save = function() {
    $scope.model.processingRequest = true;
    var request = {
			id:$scope.justification.id,
			begin:$scope.model.begin,
      end:$scope.model.end
		};

  	Assistance.requestJustificationRange($scope.model.session.user_id, request,
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















});

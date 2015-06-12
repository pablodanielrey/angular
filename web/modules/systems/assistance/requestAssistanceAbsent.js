var app = angular.module('mainApp');

app.controller('RequestAssistanceAbsentCtrl', function($scope, Assistance, Notifications, Utils) {

	$scope.model.absent = { //datos correspondientes al ausente con aviso que seran inicializados y mostrados al usuario
		id:null,       //identificacion de la justificacion
		name:null, //nombre del la justificacion
		stock:0,       //stock mensual
    yearlyStock:0  //stock anual
	};

	$scope.model.justificationAbsentRequestSelected = false;   //flag para indicar que se ha seleccionado el formulario para solicitar un ausente con aviso
	$scope.model.justificationAbsentRequestDefined = false;    //flag para indicar que se ha definido el dia de la solicitud
	$scope.model.justificationAbsentAvailableSelected = false; //flag para indicar que se ha seleccionado la seccion para ver los ausentes con aviso disponibles
	$scope.model.requestAbsentBegin = null;                    //fecha definida para la solicitud de ausente con aviso
	$scope.model.requestAbsentBeginFormated = null;            //fecha definida para la solicitud de ausente con aviso con formato amigable para el usuario


	$scope.model.processingRequest = false;




	/**
	 * Codigo a ejecutarse una vez definido el dia de la solicitud de ausente con aviso
	 */
	$scope.changeRequestAbsentBegin = function() {
		if($scope.model.requestAbsentBegin != null) {
			$scope.model.justificationAbsentRequestDefined = true;
			$scope.model.requestAbsentBeginFormated = Utils.formatDate($scope.model.requestAbsentBegin);
			return true;
		} else {
			$scope.model.justificationAbsentRequestDefined = false;
			$scope.model.requestAbsentBeginFormated = null;
			return false;
		}
	};

  /**
   * Esta seleccionada la opcion desplegable Ausente con aviso?
   * El flag de seleccion se define en el controlador padre
   * @returns {Boolean}
   */
	$scope.isSelectedJustificationAbsent = function() {
		return $scope.model.justificationAbsentSelected;
	};

  /**
   * Esta definida la fecha de solicitud de ausente con aviso?
   * @returns {Boolean}
   */
	$scope.isDefinedJustificationAbsentRequest = function() {
		return $scope.model.justificationAbsentRequestDefined;
	};

  /**
   * Esta seleccionado el formulario para definir un ausente con aviso?
   * @returns {Boolean}
   */
  $scope.isSelectedJustificationAbsentRequest = function() {
		return $scope.model.justificationAbsentRequestSelected;
	};

  /**
   * Esta seleccionado la seccion para ver los ausentes con aviso disponibles?
   * @returns {Boolean}
   */
	$scope.isSelectedJustificationAbsentAvailable = function() {
		return $scope.model.justificationAbsentAvailableSelected;
	};


  /**
   * Seleccionar y desplegar la opcion ausente con aviso
   * El flag de seleccion se define en el controlador padre
   */
	$scope.selectJustificationAbsent = function() {
		var value = !$scope.model.justificationAbsentSelected;
		$scope.clearSelections();
    $scope.clearAbsent();
		$scope.model.justificationAbsentSelected = value;
	};

  /**
   * Seleccionar y desplegar el formulario para solicitar ausente con aviso
   */
	$scope.selectJustificationAbsentRequest = function() {
		$scope.clearAbsent();
		$scope.model.justificationAbsentRequestSelected = true;
	};


  /**
   * Seleccionar y desplegar la seccion para ver los ausentes con aviso disponibles
   */
	$scope.selectJustificationAbsentAvailable = function() {
		$scope.clearAbsent();
		$scope.model.justificationAbsentAvailableSelected = true;

	};

  /**
   * Limpiar formulario
   */
	$scope.clearAbsent = function() {
		$scope.model.justificationAbsentRequestDefined = false;
		$scope.model.justificationAbsentRequestSelected = false;
		$scope.model.justificationAbsentAvailableSelected = false;
    $scope.model.requestAbsentBegin = null;
    $scope.model.requestAbsentBeginFormated = null;
	};




	//Carga el stock disponible de los ausentes con aviso
    $scope.loadAbsentStock = function(id) {
        Assistance.getJustificationStock($scope.model.session.user_id, id, null, null,
					function(justificationStock){
						$scope.model.absent.stock = justificationStock.stock;
					},
					function(error){
						//alert(error);
					}
				);
				Assistance.getJustificationStock($scope.model.session.user_id, id, null, 'YEAR',
					function(justificationStock){
						$scope.model.absent.yearlyStock = justificationStock.stock;
					},
					function(error){
						//alert(error);
					}
				);
    };


  /**
	 * Confirmar solicitud
   * Actualmente solo puede solicitar un dia a la vez
	 */
	$scope.confirmRequestAbsent = function() {

		var requestedJustification = {
			id:$scope.model.absent.id,
			begin:$scope.model.requestAbsentBegin
		};

		$scope.model.processingRequest = true;

		Assistance.requestJustification($scope.model.session.user_id, requestedJustification,null,
			function(ok) {
				$scope.model.processingRequest = false;

				$scope.clearAbsent(); //limpiar seccion de ausente con aviso
        $scope.clearSelections(); //limpiar selecciones de todas las justificaciones
        Notifications.message("Ausente con aviso cargado correctamente");
			},
			function(error){
				$scope.model.processingRequest = false;
				Notifications.message(error + ": Verifique correctamente la disponibilidad");
			}

		);
	};


	$scope.initialize = function(justification) {
    $scope.model.absent = {id:justification.id, name:justification.name, stock:0, yearlyStock:0};
		$scope.loadAbsentStock(justification.id);
	};

	// Escuchar evento de inicializacion
	$scope.$on('findStockJustification', function(event, data) {
	  if (data.justification.id == $scope.model.justificationAbsentId) {
			$scope.initialize(data.justification);
	  }
	});

	$scope.$on('JustificationStockChangedEvent', function(event, data) {
		if ($scope.model.justificationAbsentId == data.justification_id) {
			$scope.loadAbsentStock($scope.model.justificationAbsentId);
		}
	});


});

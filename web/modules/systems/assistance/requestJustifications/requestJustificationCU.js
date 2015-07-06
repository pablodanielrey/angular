
app.controller('RequestJustificationCUCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");


  $scope.rjModel = {
    id: 'b309ea53-217d-4d63-add5-80c47eb76820',
    name: Utils.getJustificationName('b309ea53-217d-4d63-add5-80c47eb76820'),
    section: null,

    date: null,
    dateFormated: null,
    processingRequest: null,

    stock: null,
    stockYear: null
  };




  /*********
   * STOCK *
   *********/
  $scope.loadStock = function(){
    Assistance.getJustificationStock($scope.model.selectedUser.id, $scope.rjModel.id, null, null,
      function(justification) {
        $scope.rjModel.stock = justification.stock;
      },
      function(error) {
        Notifications.message(error);
      }
    );

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
    $scope.loadStock();

	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
    $scope.model.justificationSelectedId = null;
    $scope.clear();
    $scope.loadStock();
	});


  $scope.$watch('model.selectedUser', function() {
    $scope.model.justificationSelectedId = null;
    $scope.clear();
    if($scope.model.selectedUser){
      $scope.loadStock();
    }
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


  /**
   * Esta seleccionado el formulario para solicitar justificaicion?
   * @returns {Boolean}
   */
	$scope.isSelectedRequest = function() {
		return ($scope.rjModel.section === "request");
	};

  /**
   * Esta seleccionada la seccion para ver la disponibilidad?
   * @returns {Boolean}
   */
  $scope.isSelectedAvailable = function() {
		return ($scope.rjModel.section === "available");
	};



  /**
   * Seleccionar formulario para definir una solicitud del articulo 102
   * @returns {Boolean}
   */
	$scope.selectRequest = function() {
    $scope.rjModel.section = "request";
	};


  /**
   * Seleccionar seccion para ver la disponibilidad correspondiente al articulo 102
   * @returns {Boolean}
   */
	$scope.selectAvailable = function() {
		$scope.rjModel.section = "available";

	};





  /********
   * DATE *
   ********/

  $scope.isDateDefined = function(){
    return ($scope.rjModel.date !== null);
  };

  $scope.selectDate = function() {
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

    Assistance.requestJustification($scope.model.selectedUser.id, request, 'PENDING',
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

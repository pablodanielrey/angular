
app.controller('RequestJustificationPECtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");


  $scope.rjModel = {
    id: 'b70013e3-389a-46d4-8b98-8e4ab75335d0',
    name: Utils.getJustificationName('b70013e3-389a-46d4-8b98-8e4ab75335d0'),
    section: null,

    begin: null,
    beginFormated: null,
    end: null,
    endFormated: null,
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
    Assistance.getJustificationStock($scope.model.selectedUser.id, $scope.rjModel.id, null, 'YEAR',
      function(justification) {
        $scope.rjModel.stockYear = justification.stock;
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
    $scope.rjModel.begin = null;
    $scope.rjModel.beginFormated = null;
    $scope.rjModel.end = null;
    $scope.rjModel.endFormated = null;
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


  $scope.isDataDefined = function(){
    return (($scope.rjModel.begin !== null) && ($scope.rjModel.end !== null));
  };

  $scope.selectDate = function(){
    if($scope.rjModel.end !== null){
      if(($scope.rjModel.begin !== null) && ($scope.rjModel.begin > $scope.rjModel.end)){
        $scope.rjModel.end = new Date($scope.rjModel.begin);
      }
    }

    $scope.rjModel.beginFormated = null;
    if($scope.rjModel.begin !== null){
			$scope.rjModel.beginFormated = Utils.formatDate($scope.rjModel.begin);
    }

    $scope.rjModel.endFormated = null;
    if($scope.rjModel.end !== null){
			$scope.rjModel.endFormated = Utils.formatDate($scope.rjModel.end);
    }
  };




  $scope.save = function() {

   $scope.rjModel.processingRequest = true;

    var request = {
			id:$scope.rjModel.id,
			begin:$scope.rjModel.begin,
      end:$scope.rjModel.end,
		};

    Assistance.requestJustificationRange($scope.model.selectedUser.id, request, 'PENDING',
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

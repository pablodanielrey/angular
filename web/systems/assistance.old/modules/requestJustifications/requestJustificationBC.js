
app.controller('RequestJustificationBCCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");


  $scope.rjModel = {
    id: 'cb2b4583-2f44-4db0-808c-4e36ee059efe',
    name: Utils.getJustificationName('cb2b4583-2f44-4db0-808c-4e36ee059efe'),

    date: null,
    dateFormated: null,
    begin: null,
    beginFormated: null,
    processingRequest: null,

  };







  /******************
   * INICIALIZACION *
   ******************/
  $scope.clear = function(){
    $scope.rjModel.date = null;
    $scope.rjModel.dateFormated = null;
    $scope.rjModel.begin = null;
    $scope.rjModel.beginFormated = null;
    $scope.rjModel.processingRequest = false;

  };


  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, args) {
    data = args[0];
    if ($scope.rjModel.id == data.justification_id) {
      $scope.model.justificationSelectedId = null;
      $scope.clear();
    }
	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
    $scope.model.justificationSelectedId = null;
    $scope.clear();

	});


  $scope.$watch('model.selectedUser', function() {
    $scope.model.justificationSelectedId = null;
    $scope.clear();

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




  /**************
   * FORMULARIO *
   **************/

  $scope.isDataDefined = function(){
    return ($scope.rjModel.date !== null) && ($scope.rjModel.begin !== null) && ($scope.rjModel.end !== null);
  };

  $scope.defineData = function() {
    $scope.rjModel.dateFormated = null;
    if($scope.rjModel.date !== null){
			$scope.rjModel.dateFormated = Utils.formatDate($scope.rjModel.date);
    }

    $scope.rjModel.beginFormated = null;
    if($scope.rjModel.begin !== null){
			$scope.rjModel.beginFormated = Utils.formatTime($scope.rjModel.begin);
    }

  };



  $scope.save = function() {

   $scope.rjModel.processingRequest = true;

    var request = {
			id:$scope.rjModel.id,
			begin: new Date($scope.rjModel.date),
		};

   request.begin.setHours($scope.rjModel.begin.getHours(), $scope.rjModel.begin.getMinutes());

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

var app = angular.module('mainApp');

app.controller('UsersAssistanceManagementMediatorRequestJustificationCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");


  $scope.init = function(justificationId){
    //***** inicializar datos de la justificacion *****
    $scope.justification = {
      id: justificationId, //id de la justificacion
      name:Utils.getJustificationName(justificationId),
      stock:0,
      yearlyStock:0
    };
  };
  

  //***** variables del formulario *****  
  $scope.model.begin = null;         //fecha seleccionada
  $scope.model.beginFormated = null; //fecha en formato amigable para el usuario
  $scope.model.end = null;         //fecha seleccionada
  $scope.model.endFormated = null; //fecha en formato amigable para el usuario
  
  $scope.model.processingRequest = false;
  
  

  //***** METODOS DE SELECCION DE LA SECCION *****
  /**
   * Esta seleccionada la seccion correspondiente a la justificacion?
   * @returns {Boolean}
   */
  $scope.isSelectedJustification = function() {
    return ($scope.model.justificationSelectedId === $scope.justification.id);
  };

  /**
   * Modificar seleccion de opcion desplegable correspondiente a salidas eventuales
   * @returns {Boolean}
   */
	$scope.selectJustification = function() {
    $scope.clearContent();
    if($scope.model.justificationSelectedId === $scope.justification.id){
      $scope.model.justificationSelectedId = null;
    } else {
       $scope.model.justificationSelectedId = $scope.justification.id;
    }
	};
  
  
  /**
   * Inicializar variables correspondientes al contenido de la seccion del articulo 102
   * @returns {undefined}
   */
  $scope.clearContent = function(){
    $scope.model.begin = null;
		$scope.model.beginFormated = null;
    $scope.model.end = null;
		$scope.model.endFormated = null;
    $scope.model.processingRequest = false;
    
  };
  
    
    
  //***** METODOS DEl FORMULARIO DE SOLICITUD *****
  $scope.selectDates = function(){
		$scope.model.beginFormated = null;
    if($scope.model.begin !== null){
			$scope.model.beginFormated = Utils.formatDate($scope.model.begin);
    }
    if($scope.model.end !== null){
      if(($scope.model.begin !== null) && ($scope.model.begin > $scope.model.end)){
        $scope.model.end = new Date($scope.model.begin);
      }
      $scope.model.endFormated = Utils.formatDate($scope.model.end);

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
      end:$scope.model.end,
		};
    console.log(request);
    console.log($scope.model.user.id);
    
  	Assistance.requestJustification($scope.model.user.id, request,
			function(ok) {
				$scope.clearContent();    //limpiar contenido
        $scope.model.justificationSelectedId = null; //limpiar selecciones
        Notifications.message("Solicitud de " + $scope.justification.name + " registrada correctamente");
			},
			function(error){
        $scope.clearContent();    //limpiar contenido
       $scope.model.justificationSelectedId = null; //limpiar selecciones
				Notifications.message(error);
			}

		);

  };

}]);

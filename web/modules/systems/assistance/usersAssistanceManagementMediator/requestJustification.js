var app = angular.module('mainApp');

app.controller('UsersAssistanceManagementMediatorRequestJustificationCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");
  
  //***** variables de seleccion de la seccion *****
  $scope.model.requestSelected = false; //flag para indicar la seleccion del formulario de solicitud
  $scope.model.availableSelected = false; //flag para indicar la seleccion de la visualizacion de disponibilidad
 
  $scope.init = function(justificationId){

    //***** inicializar datos de la justificacion *****
    $scope.justification = {
       id: justificationId,
       name: Utils.getJustificationName(justificationId),
       requestMode: Utils.getJustificationRequestMode(justificationId),
       stockMode: Utils.getJustificationStockMode(justificationId),
       mode:  Utils.getJustificationRequestMode(justificationId) + "," + Utils.getJustificationStockMode(justificationId),
       stock: null,
       stockYear: null
    };

  };
   
  
  
  $scope.clearSections = function(){
    $scope.model.requestSelected = false;
    $scope.model.availableSelected = false;
  };
  
  
  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, data){
    $scope.model.justificationSelectedId = null;
    $scope.clearSections();

	});

	$scope.$on('JustificationStatusChangedEvent', function(event, data) {
    $scope.model.justificationSelectedId = null;
    $scope.clearSections();
	});
  
  
  $scope.$watch('model.selectedUser', function() {
    $scope.model.justificationSelectedId = null;
    $scope.clearSections();
  }); 
  
  $scope.$watch('model.justificationSelectedId', function() {
    $scope.clearSections();
  });
  
  
  
  
  //***** METODOS DE SELECCION DE LA SECCION *****
  /**
   * Esta seleccionada la seccion correspondiente a la justificacion?
   * @returns {Boolean}
   */
  $scope.isSelectedJustification = function() {
    return ($scope.model.justificationSelectedId === $scope.justificationId);
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
    if($scope.model.justificationSelectedId === $scope.justification.id){
      $scope.model.justificationSelectedId = null;
    } else {
      $scope.model.justificationSelectedId = $scope.justification.id;
    }
	};
  



  /*******************************
   * METODOS DE ACCESO AL SERVER *
   *******************************/
  $scope.loadStockTotal = function(){
    Assistance.getJustificationStock($scope.model.selectedUser.id, $scope.justification.id, null, null,
      function(justification) {
        $scope.justification.stock = justification.stock;
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };
  
  
  $scope.loadStockTotalTime = function(){
    Assistance.getJustificationStock($scope.model.selectedUser.id, $scope.justification.id, null, null,
      function(justification) {
        $scope.justification.stock = Utils.getTimeFromSeconds(justification.stock);
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };
  
 
  
  
  $scope.loadStockYear = function(){

    Assistance.getJustificationStock($scope.model.selectedUser.id, $scope.justification.id, null, 'YEAR',
      function(justification) {
        $scope.justification.stockYear = justification.stock;
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };
  

  
  /*************************************
   * METODOS DE SELECCION DE SECCIONES *
   *************************************/
  
  /**
   * Esta seleccionado el formulario para solicitar justificaicion?
   * @returns {Boolean}
   */
	$scope.isSelectedRequest = function() {
		return $scope.model.requestSelected;
	};

  /**
   * Esta seleccionada la seccion para ver la disponibilidad?
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
    $scope.model.availableSelected = false;
		$scope.model.requestSelected = true;
	};


  /**
   * Seleccionar seccion para ver la disponibilidad correspondiente al articulo 102
   * @returns {Boolean}
   */
	$scope.selectAvailable = function() {
		$scope.model.requestSelected = false;
		$scope.model.availableSelected = true;

	};
  
}]);

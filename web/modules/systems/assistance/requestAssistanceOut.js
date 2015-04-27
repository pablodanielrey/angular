var app = angular.module('mainApp');

app.controller('RequestAssistanceOutCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {


  $scope.model.out = {  //datos correspondientes a la salida eventual que seran mostrados al usuario
    id:null,       //identificacion de la justificacion
    name:null,
		stock:0,       //stock mensual
    yearlyStock:0  //stock anual
  };
  
  $scope.model.justificationOutRequestSelected = false;   //flag para indicar si esta seleccionado el formulario para solicitar una salida eventual
  $scope.model.justificationOutAvailableSelected = false; //flag para indicar si esta seleccionada la seccion para visualizar las salidas eventuales disponibles
  $scope.model.date = null;           //fecha de la salida eventual a solicitar
  $scope.model.begin = null;          //hora de inicio de la salida eventual a solicitar
  $scope.model.end = null;            //hora de fin de la salida eventual a solicitar
  $scope.model.dateFormated = null;   //fecha de la salida eventual a solicitar en un formato amigable para el usuario
  $scope.model.beginFormated = null;  //hora de inicio de la salida eventual a solicitar en un formato amigable para el usuario
  $scope.model.endFormated = null;    //hora de fin de la salida eventual a solicitar en un formato amigable para el usuario
  $scope.model.timeFormated = null;   //diferencia de tiempo para ser mostrada al usuario

    // ---------------- Manejo de la vista --------------------

  /**
   * Esta seleccionada la seccion correspondiente a salidas eventuales
   * @returns {Boolean}
   */
  $scope.isSelectedJustificationOut = function() {
    return $scope.model.justificationOutSelected;
  };

  /**
   * Modificar seleccion de opcion desplegable correspondiente a salidas eventuales
   * @returns {Boolean}
   */
	$scope.selectJustificationOut = function() {
    var value = !$scope.model.justificationOutSelected;
    $scope.clearSelections();
    $scope.clearOut();
    $scope.model.justificationOutSelected = value;
	};

 /**
   * Esta seleccionada el formulario para definir una salida eventual?
   * @returns {Boolean}
   */
	$scope.isSelectedJustificationOutRequest = function() {
		return $scope.model.justificationOutRequestSelected;
	};

  /**
   * Esta seleccionada la seccion para ver las salidas eventuales disponibles
   * @returns {Boolean}
   */
  $scope.isSelectedJustificationOutAvailable = function() {
		return $scope.model.justificationOutAvailableSelected;
	};


  /**
   * Seleccionar formulario para definir una solicitud de salida eventual
   * @returns {Boolean}
   */
	$scope.selectJustificationOutRequest = function() {
		$scope.clearOut();
		$scope.model.justificationOutRequestSelected = true;
	};


  /**
   * Seleccionar seccion para ver las salidas eventuales disponibles
   * @returns {Boolean}
   */
	$scope.selectJustificationOutAvailable = function() {
		$scope.clearOut();
		$scope.model.justificationOutAvailableSelected = true;

	};

  /**
   * Limpiar opciones correspondientes a la seccion de salida eventual
   * @returns {Boolean}
   */
	$scope.clearOut = function() {
		$scope.model.justificationOutRequestSelected = false;
		$scope.model.justificationOutAvailableSelected = false;
    $scope.model.date = null;
    $scope.model.begin = null;
    $scope.model.end = null;
    $scope.model.dateFormated = null;
    $scope.model.beginFormated = null;
    $scope.model.endFormated = null;
    $scope.model.timeFormated = null;
      
  
	};


    /**
     * Esta definida la solicitud de salida eventual correctamente?
     * @returns {Boolean}
     */
    $scope.isOutDefined = function(){
      if ($scope.model.date && $scope.model.begin && $scope.model.end) {
          return true;
      } else {
         return false;
      }  
    };

    /**
     * Define los datos de salida eventual a medida que el usuario va completando el formulario
     * @returns {Boolean}
     */
    $scope.defineOut = function() {
        if ($scope.model.date) $scope.model.dateFormated = Utils.formatDate($scope.model.date);
        if ($scope.model.begin) $scope.model.beginFormated = Utils.formatTime($scope.model.begin);
        if ($scope.model.begin && $scope.model.end) {
          if($scope.model.begin > $scope.model.end) $scope.model.end = $scope.model.begin;
        }
        if ($scope.model.end) $scope.model.endFormated = Utils.formatTime($scope.model.end);
        if ($scope.model.begin && $scope.model.end) $scope.model.timeFormated = Utils.getDifferenceTimeFromDates($scope.model.begin, $scope.model.end);
    };




    // ------------------------------------------------------------------------


    /*
    parsea segundos a un formato imprimible en horas.
    para las boletas de salida.
    lo saque de :
    http://stackoverflow.com/questions/6312993/javascript-seconds-to-time-string-with-format-hhmmss
    */
    $scope.parseSecondsToDateString = function(sec) {
      var hours   = Math.floor(sec / 3600);
      var minutes = Math.floor((sec - (hours * 3600)) / 60);
      var seconds = sec - (hours * 3600) - (minutes * 60);

      if (hours   < 10) {hours   = "0"+hours;}
      if (minutes < 10) {minutes = "0"+minutes;}
      if (seconds < 10) {seconds = "0"+seconds;}
      var time    = hours+':'+minutes;
      return time;
    };


    //Carga el stock disponible
    $scope.loadOutStock = function(id) {
      Assistance.getJustificationStock($scope.model.session.user_id, id, null, null,
        function(justification) {
          $scope.model.out.stock = $scope.parseSecondsToDateString(justification.stock);
        },
        function(error) {
          Notifications.message(error);
        }
      );
      Assistance.getJustificationStock($scope.model.session.user_id, id, null, 'YEAR',
        function(justification) {
          $scope.model.out.yearlyStock = $scope.parseSecondsToDateString(justification.stock);
        },
        function(error) {
          Notifications.message(error);
        }
      );
    };


    // Cargo el stock de la justificacion
    // data.justification = {name,id}
    $scope.$on('findStockJustification', function(event, data) {
        if (data.justification.id == $scope.model.justificationOutId) {
            $scope.initialize(data.justification);
        }
    });

    $scope.$on('JustificationStockChangedEvent', function(event, data) {
 
      if ($scope.model.justificationOutId == data.justification_id) {
        $scope.loadOutStock($scope.model.justificationOutId);
      }
    });



    $scope.initialize = function(justification) {
        $scope.model.out = {id:justification.id, name: justification.name, stock:0, yearlyStock:0};
        $scope.loadOutStock(justification.id);
    };

   
    // Envio la peticion al servidor
    $scope.save = function() {

      var requestedJustification = {
        id:$scope.model.out.id,
        begin: new Date($scope.model.date),
        end: new Date($scope.model.date)
      };
      
      requestedJustification.begin.setHours($scope.model.begin.getHours(), $scope.model.begin.getMinutes());
      requestedJustification.end.setHours($scope.model.end.getHours(), $scope.model.end.getMinutes());

      
      Assistance.requestJustification($scope.model.session.user_id,requestedJustification,
          function(ok) {
            $scope.clearOut();
            $scope.clearSelections(); //limpiar selecciones de todas las justificaciones
            Notifications.message("Salida eventual cargada correctamente");
          },
          function(error) {
              Notifications.message(error + ": Verifique correctamente la disponibilidad");
          }
      );
    };

}]);

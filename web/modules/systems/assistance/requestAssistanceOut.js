var app = angular.module('mainApp');

app.controller('RequestAssistanceOutCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {


    $scope.model.justificationOutRequestSelected = false;
    $scope.model.justificationOutAvailableSelected = false;
    $scope.model.justificationOutRequestsSelected = false;

    // ---------------- Manejo de la vista --------------------

  $scope.isSelectedJustificationOut = function() {
    return $scope.model.justificationOutSelected;
  };

	$scope.selectJustificationOut = function() {
    var value = !$scope.model.justificationOutSelected;
    $scope.clearSelections();
    $scope.clearSelectionsOut();
    $scope.model.justificationOutSelected = value;

    $scope.model.justification.id = $scope.model.justificationOutId;
	};

	$scope.isSelectedJustificationOutRequest = function() {
		return $scope.model.justificationOutRequestSelected;
	};

    $scope.isSelectedJustificationOutAvailable = function() {
		return $scope.model.justificationOutAvailableSelected;
	};

	$scope.isSelectedJustificationOutRequests = function() {
		return $scope.model.justificationOutRequestsSelected;
	};

	$scope.selectJustificationOutRequest = function() {
		$scope.clearSelectionsOut();
		$scope.model.justificationOutRequestSelected = true;
	};


	$scope.selectJustificationOutRequests = function() {
		$scope.clearSelectionsOut();
		$scope.model.justificationOutRequestsSelected = true;
	};

	$scope.selectJustificationOutAvailable = function() {
		$scope.clearSelectionsOut();
		$scope.model.justificationOutAvailableSelected = true;

	};


	$scope.clearSelectionsOut = function() {
		$scope.model.justificationOutRequestSelected = false;
		$scope.model.justificationOutAvailableSelected = false;
		$scope.model.justificationOutRequestsSelected = false;

    if ($scope.model.justification != null) {
        $scope.model.justification.begin = null;
        $scope.model.justification.end = null;
    }
	};



    $scope.isOutDefined = function(){
      if ($scope.model.date && $scope.model.begin && $scope.model.end) {
          return true;
      } else {
         return false;
      }  
    };

    /**
     * Define una salida eventual en funcion de los datos ingresados por el usuario
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
        
        
        if($scope.isOutDefined()){
            $scope.model.justification.begin = new Date($scope.model.date);
            $scope.model.justification.begin.setHours($scope.model.begin.getHours(), $scope.model.begin.getMinutes());
            $scope.model.justification.end = new Date($scope.model.date);
            $scope.model.justification.end.setHours($scope.model.end.getHours(), $scope.model.end.getMinutes());
        }
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
        justification = data.justification;
        if (justification.id == $scope.model.justificationOutId) {
            $scope.initialize(justification);
        }
    });

    $scope.$on('JustificationStockChangedEvent', function(event, data) {
      if ($scope.model.justificationOutId == data.justification_id) {
        $scope.loadOutStock($scope.model.justificationOutId);
      }
    });



    $scope.initialize = function(justification) {
        $scope.clearSelectionsOut();
        $scope.model.out = {id:justification.id, name: justification.name, stock:0};
        $scope.loadOutStock(justification.id);
        $scope.model.justification = {id:justification.id,begin:null,end:null,hours:0};
    };

   
    // Envio la peticion al servidor
    $scope.save = function() {

        Assistance.requestJustification($scope.model.session.user_id,$scope.model.justification,
            function(ok) {
              // nada
            },
            function(error) {
                Notifications.message(error);
            }
        );
    };

}]);

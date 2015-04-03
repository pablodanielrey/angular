var app = angular.module('mainApp');

app.controller('RequestAssistanceOutCtrl', function($scope, Assistance, Notifications) {


    $scope.model.justificationOutRequestSelected = false;
    $scope.model.justificationOutAvailableSelected = false;
    $scope.model.justificationOutRequestsSelected = false;

    // ---------------- Manejo de la vista --------------------

  $scope.isSelectedJustificationOut = function() {
    return $scope.model.justificationOutSelected;
  }

	$scope.selectJustificationOut = function() {
    var value = !$scope.model.justificationOutSelected;
    $scope.clearSelections();
    $scope.clearSelectionsOut();
    $scope.model.justificationOutSelected = value;

    $scope.model.justification.id = $scope.model.justificationOutId;
	}

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
	}

    $scope.isSelectedDate = function() {
        if ($scope.model.justification != null && $scope.model.justification.begin != null) {
            $scope.dateFormated = $scope.model.justification.begin.toLocaleDateString();

            var hoursBegin = ('0'+$scope.model.justification.begin.getHours()).substr(-2);
            var minutesBegin = ('0'+$scope.model.justification.begin.getMinutes()).substr(-2);
            $scope.dateFormated += " " + hoursBegin + ":" + minutesBegin;

            if ($scope.model.justification.end != null) {
                var hoursEnd = ('0'+$scope.model.justification.end.getHours()).substr(-2);
                var minutesEnd = ('0'+$scope.model.justification.end.getMinutes()).substr(-2);
                $scope.dateFormated += "-" + hoursEnd + ":" + minutesEnd;
            }

            return true;
        } else {
            $scope.dateFormated = null;
            return false;
        }
    }

    $scope.changeHours = function() {
        if ($scope.model.justification.begin ==  null && $scope.model.justification.end == null) {
            $scope.model.justification.totalHours = 0;
            return;
        }

        if (($scope.model.justification.end == null) || ($scope.model.justification.end < $scope.model.justification.begin)) {
            $scope.model.justification.end = $scope.model.justification.begin;
        }

        var totalDate = $scope.model.justification.end - $scope.model.justification.begin;
        var min = ((totalDate/(1000*60))%60);
        var hours = ~~(totalDate / (1000*60*60));
        $scope.model.justification.totalHours =  ('0'+hours).substr(-2) + ":" + ('0'+min).substr(-2);
    }


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
    }


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
    }


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
    }

    $scope.changeDate = function() {
        if ($scope.model.justification.begin == null) {
            return;
        }

        if ($scope.model.justification.end == null) {
          $scope.model.justification.end = $scope.model.justification.begin;
        } else {
            var aux = $scope.model.justification.end;
            $scope.model.justification.end = new Date($scope.model.justification.begin.getTime());
            $scope.model.justification.end.setHours(aux.getHours());
            $scope.model.justification.end.setMinutes(aux.getMinutes());
        }
    }

    // Envio la peticion al servidor
    $scope.save = function() {

        Assistance.requestJustification($scope.model.session.user_id,$scope.model.justification,
            function(ok) {
                Notifications.message("Guardado exitosamente");
                $scope.clearSelections();
            },
            function(error) {
                Notifications.message(error);
            }
        );
    }

});

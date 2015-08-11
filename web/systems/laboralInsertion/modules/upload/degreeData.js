var app = angular.module('mainApp');

app.controller('DegreeLaboralInsertionCtrl', function($scope, $timeout, LaboralInsertion) {

  $scope.$on('UpdateUserDataEvent',function(event,data) {
    $scope.loadData();
  });

	$scope.$on('EditInsertionCheckDataEvent',function() {
		$scope.model.status.degrees = true;
		$scope.$emit("EditInsertionDataCheckedEvent");
	});


  $scope.onDegreeChange = function(degree) {
    $scope.onCoursesChange(degree);
  }


  /*
    para implementar el chequeo que quiere lucas de las ofertas.
  */
  $scope.onCoursesChange = function(degree) {
    var show = false;
    if (degree.name == 'Contador Público') {
      show = (degree.courses >= 29);

    } else if (degree.name == 'Licenciado en Administración') {
      show = (degree.courses >= 32);

    } else if (degree.name == 'Licenciado en Turismo') {
      show = (degree.courses >= 20);

    } else if (degree.name == 'Licenciado en Economía') {
      show = (degree.courses >= 30);

    } else if (degree.name == 'Técnico en Cooperativas') {
      show = (degree.courses >= 15);
    }

    if (!show) {
      degree.offerYoungProfessionals = false;
    }
    degree.showOfferYoungProfessionals = show;
  }


  $scope.addDegree = function() {
    var degree = {
      id: null,
      user_id: $scope.model.selectedUser,
      name: '',
      courses: 0,
      average1: 0,
      average2: 0,
      showOfferYoungProfessionals: false
    }
    $scope.model.degrees.push(degree);
  }

  $scope.deleteDegree = function($index) {
		$scope.model.degrees.splice($index, 1);
		if ($scope.model.degrees.length == 0) {
      		$scope.addDegree()
    	}
	}

  $scope.loadData = function() {

    LaboralInsertion.findDegreeData($scope.model.selectedUser,
      function(data) {
    		if ((data != undefined) && (data != null) && (data.length > 0)) {
    			$scope.model.degrees = data;
    			$scope.extendWorkType();

    		}
    		if ($scope.model.degrees.length == 0) {
    			$scope.addDegree()
    		}
      },
      function(err) {
        //alert(err);
      });

  }

 	 /**
	 * Transformar datos de degree. La oferta seleccionada se transfora en su correspondiente valor string
	 * @private
	 */
	$scope.extendWorkType = function() {
		for (var i = 0; i < $scope.model.degrees.length; i++) {
			$scope.model.degrees[i].offerInternship = false;
			$scope.model.degrees[i].offerFullTime = false;
			$scope.model.degrees[i].offerYoungProfessionals = false;
      $scope.model.degrees[i].showOfferYoungProfessionals = false;

			if($scope.model.degrees[i].work_type.indexOf("Internship") > -1){
				$scope.model.degrees[i].offerInternship = true;
			}
			if($scope.model.degrees[i].work_type.indexOf("FullTime") > -1){
				$scope.model.degrees[i].offerFullTime = true;
			}
			if($scope.model.degrees[i].work_type.indexOf("YoungProfessionals") > -1){
				$scope.model.degrees[i].offerYoungProfessionals = true;
        $scope.model.degrees[i].showOfferYoungProfessionals = true;
			}
		}
	};

  $timeout(function() {
    $scope.loadData();
  });


	$scope.showOfferYoungProffesionals = function(degree){

    return degree.showOfferYoungProfessionals;
    /*
    Contador Público >= 28
    Licenciado en Administración >= 30
    Licenciado en Turismo >= 24
    Licenciado en Economía >= 29
    Técnico en Cooperativas >= 16

    cantidad de materias como máximo 37
    */
    /*
		if(degree.courses > 29){
			return true;
		} else {
			return false;
		}
    */
	};

});

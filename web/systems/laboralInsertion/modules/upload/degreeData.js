var app = angular.module('mainApp');

app.controller('DegreeLaboralInsertionCtrl', function($scope, LaboralInsertion) {

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
	}


  /**
	 * Transformar datos de degree. La oferta seleccionada se transfora en su correspondiente valor string
	 * @private
	 */
	$scope.transformDegreeData = function() {
		for (var i = 0; i < $scope.model.degrees.length; i++) {

			if($scope.model.degrees[i].name == ""){
				Notifications.message('Debe seleccionar carrera');
				$scope.model.status = false;
			}

			if(isNaN($scope.model.degrees[i].courses)){
				$scope.model.degrees[i].courses = 0;
			}

			if(isNaN($scope.model.degrees[i].average1)){
				$scope.model.degrees[i].average1 = 0;
			}

			if(isNaN($scope.model.degrees[i].average2)){
				$scope.model.degrees[i].average2 = 0;
			}

			$scope.model.degrees[i].work_type = '';
			if ($scope.model.degrees[i].offerInternship) {

				$scope.model.degrees[i].work_type += 'Internship;';
			}
			if ($scope.model.degrees[i].offerFullTime) {
				$scope.model.degrees[i].work_type += 'FullTime;';
			}
			if ($scope.model.degrees[i].offerYoungProfessionals) {
				$scope.model.degrees[i].work_type += 'YoungProfessionals;';
			}
		}
	};


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


	$scope.showOfferYoungProffesionals = function(degree){
    return degree.showOfferYoungProfessionals;
	};

  $scope.initialize = function() {
    $scope.$parent.transformations.push($scope.transformDegreeData);
  };

  $scope.$parent.$on('$viewContentLoaded', function(event) {
		$scope.initialize();
	});

});

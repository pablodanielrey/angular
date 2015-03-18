var app = angular.module('mainApp');

app.controller('EditInsertionDataCtrl',function($scope, $timeout, $location, Session, Users, Student, LaboralInsertion) {

	$scope.model = {
		insertionData: {},
		degrees: [],
		languages: [],
		userData: {},
		studentData : {},
		selectedUser: null,
		//status: {profile:false, languages:false, degrees:false, insertion:false} //objeto para indicar si los datos de lenguajes estan en condiciones de guardarse, el objeto sera modificado en los subcontroladores
	};


	/**
	 * Al guardar datos se debe disparar un evento de chequeo que sera escuchado por cada subcontrolador
	 *
	$scope.check = function() {
		$scope.$broadcast('EditInsertionCheckDataEvent');
	};*/

	/**
	 * Escuchar evento de finalizacion de chequeo de datos. Los subcontroladores al finalizar el chequeo dispararan el evento de finalizacion de chequeo de datos.
	 *
	$scope.$on('EditInsertionDataCheckedEvent',function() {
	
		if($scope.model.status.profile
		&& $scope.model.status.languages
		&& $scope.model.status.degrees
		&& $scope.model.status.insertion){
			console.log($scope.model.status);
			$scope.save();
		}
		
	});*/
	
	
	$scope.saveUser = function(){
		
		$scope.transformProfileData();
		
		// actualizo los datos del perfil.
		Users.updateUser($scope.model.userData,
			function(ok) {
			},
			function(error) {
				alert(error);
			}
		);
	
	};
	
	$scope.saveInsertionData = function(){
		$scope.transformInsertionData();
		
		$scope.model.insertionData.id = $scope.model.userData.id;
		
		LaboralInsertion.updateLaboralInsertionData($scope.model.insertionData,
			function(ok) {
			},
			function(error) {
				alert(error);
			}
		);
	
	};
	
	$scope.saveLanguages = function(){

		LaboralInsertion.updateLanguageData($scope.model.userData.id, $scope.model.languages,
			function(ok) {
			},
			function(error) {
				alert(error);
			}
		);
	};
	
	/**
	 * Guardar datos de degrees
	 * @protected
	 */
	$scope.saveDegrees = function(){
	
		$scope.transformDegreeData();

		LaboralInsertion.updateDegreeData($scope.model.userData.id, $scope.model.degrees,
			function(ok) {
			},
			function(error) {
				alert(error);
			}
		);
	};

	/**
	 * Transformar datos de degree. La oferta seleccionada se transfora en su correspondiente valor string
	 * @private
	 */
	$scope.transformDegreeData = function() {
		for (var i = 0; i < $scope.model.degrees.length; i++) {
			
			if($scope.model.degrees[i].name == ""){
				alert("Debe seleccionar carrera");
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
	 * Transformar datos de profile
	 */
	$scope.transformProfileData = function(){
		
		
		$scope.model.userData.telephones = [];
		
		if($scope.model.userData.cellPhone){
			var telephone = {
				type:"cell",
				number:$scope.model.userData.cellPhone.country + " " + $scope.model.userData.cellPhone.city + " 15 " + $scope.model.userData.cellPhone.number,
			};
			$scope.model.userData.telephones.push(telephone);
		}
		
		if($scope.model.userData.homePhone){
			var telephone = {
				type:"home",
				number:$scope.model.userData.homePhone.country + " " + $scope.model.userData.homePhone.city + " " + $scope.model.userData.homePhone.number,
			};
			$scope.model.userData.telephones.push(telephone);
		}
	};
	
	
	/**
	 * Transformar datos de insercion
	 */
	$scope.transformInsertionData = function(){
		
		if($scope.model.insertionData.travel === ""){
			$scope.model.insertionData.travel = false;

		
		}
		if($scope.model.insertionData.reside === ""){
			$scope.model.insertionData.reside = false;
		}
		
		if($scope.model.insertionData.cv === ""){
			alert("Debe cargar su CV");
		}
	};

	
	$scope.save = function() {
		$scope.saveUser	();
		$scope.saveInsertionData();
		$scope.saveLanguages();
		$scope.saveDegrees();
		alert("Sus datos han sido registrados");
	};





	/**
	 * procesar verificacion de terminos y condiciones
	 */
	$scope.checkTermsAndConditions = function() {

		LaboralInsertion.isTermsAndConditionsAccepted($scope.model.selectedUser,
			function(response) {
				if(!response.accepted) {
					$location.path('/acceptTermsAndConditionsInsertion');
				}
			},
			function(error) {
				$location.path('/main');
			}
		);

	};

	$scope.initialize = function() {
		// seteo el usuario seleccionado dentro del scope para que lo usen las subvistas facilmente.
		var s = Session.getCurrentSession();
		if (s == null) {
		  $location.path('/main');
		}
		if (s.selectedUser == undefined || s.selectedUser == null) {
		  s.selectedUser = s.user_id;
  		  Session.saveSession(s);
		}
		$scope.model.selectedUser = s.selectedUser;
		$scope.checkTermsAndConditions();
		$scope.$broadcast('UpdateUserDataEvent');
	};


	$timeout(function() {
		$scope.initialize();
		
	});


});

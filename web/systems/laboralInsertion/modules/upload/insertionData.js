
var app = angular.module('mainApp');

app.controller('LaboralInsertionDataCtrl', function($scope, $timeout, LaboralInsertion, Files, Notifications) {

	$scope.model.cv = {
		loading: false
	};

	/**
	 * Agregar cv como base 64
	 */
	$scope.addCv = function(fileName, fileContent) {
		$scope.model.cv.loading = true;

		var cv = window.btoa(fileContent)
		Files.upload(null, fileName, cv,
			function(id) {
				console.log('archivo subido correctamente con el id : ' + id);
				Notifications.message('archivo : ' + id);
			},
			function(err) {
				Notifications.message(err);
			}
		);

	};


	$scope.downloadCV = function() {
		LaboralInsertion.findLaboralInsertionCV($scope.model.selectedUser,
			function(data) {
				if (data == undefined) {
					Notifications.message('No tiene CV cargado');
					return;
				}

				/*
					esto es necesario para convertir el base64 en un array de bytes para el Blob
				*/
				var binary = atob(data.cv);
				var array = new Uint8Array(binary.length);
				for( var i = 0; i < binary.length; i++ ) { array[i] = binary.charCodeAt(i); };
				window.saveAs(new Blob([array],{type: "octet/stream;base64"}),data.name);

			},
			function(err) {
				Notifications.message(err);
			});
	}



	$scope.initialize = function() {
    $scope.model.cv = {
			loading: false
		};
  };

  $scope.$parent.$on('$viewContentLoaded', function(event) {
		$scope.initialize();
	});

});


var app = angular.module('mainApp');

app.controller('LaboralInsertionDataCtrl', function($scope, $timeout, LaboralInsertion, Notifications) {

	/**
	 * Agregar cv como base 64
	 */
	$scope.addCv = function(fileName,fileContent){
		var cv = window.btoa(fileContent)
		var data = {
			'id': $scope.model.userData.id,
			'cv':cv,
			'name': fileName
		}
		LaboralInsertion.updateLaboralInsertionCV(data,
			function(ok) {
				Notifications.message('Cv cargado correctamente');
			},
			function(error){
				Notifications.message(error);
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


  $scope.loadData = function() {

    LaboralInsertion.findLaboralInsertionData($scope.model.selectedUser,
      function(data) {
        $scope.model.insertionData = data;
      },
      function(err) {
        Notifications.message(err);
      });


			/*
			LaboralInsertion.findLaboralInsertionCV($scope.model.selectedUser,
				function(data) {
					//$scope.model.cv.c = 'data:application/octet-stream;base64,' + data.cv;
					$scope.model.cv.c = window.URL.createObjectURL(new Blob([data.cv],{type: "octet/stream", encoding: 'base64'}));
					$scope.model.cv.loaded = true;
				},
				function(err) {
					Notifications.message(err);
				});
			*/

  }

  $scope.$on('UpdateUserDataEvent',function(event,data) {
    $scope.loadData();
  });


  $timeout(function() {
    $scope.loadData();
  });

});

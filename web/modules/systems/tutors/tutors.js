
var app = angular.module('mainApp');

app.controller('TutorsCtrl', function($rootScope,$scope,$timeout,Student,Session,Profiles,Tutors,Notifications) {

  $scope.model = {
    register:{ type:'', student:{}, date:new Date() }
  };

  $scope.displayExport = false;


  $scope.clearData = function() {
    $scope.model.register = { type:'', student:{}, date:new Date() };
    $scope.displayExport = false;
  }

  $timeout(function() {
    $scope.clearData();
    $scope.checkAccess();
  });

  $scope.showDisplayExport = function() {
    console.log("Value:"+$scope.displayExport);
    return $scope.displayExport;
  }
  $scope.checkAccess = function() {
    Profiles.checkAccess(Session.getSessionId(),'ADMIN-TUTOR', function(ok) {
      if (ok == 'granted') {
        $scope.displayExport = true;
      } else {
        $scope.displayExport = false;
      }
    },
    function(error) {
      $scope.displayExport = false;
    });

  }

  $scope.save = function() {
    Tutors.persistTutorData($scope.model.register,
      function(ok) {
        $scope.clearData();
        Notifications.message(ok);
      },
      function(error) {
        Notifications.message(error);
      }
    );
  }



  $scope.export = function() {
    Tutors.listTutorData(
			function(data){
        $scope.exportToCsv(data);
			},
			function(error){
				alert(error);
			}
		);
  }


  $scope.exportToCsv = function(data) {
    var csvString = "Fecha,Apellido,Nombre,Legajo,Dni,Tipo\n";

    for (var i = 0; i < data.length; i++) {
      var date = new Date(data[i]["date"]);
      var row = "";
      row += date.toLocaleDateString();
      row += "," + data[i]["student"]["lastname"];
      row += "," + data[i]["student"]["name"];
      row += "," + data[i]["student"]["studentNumber"];
      row += "," + data[i]["student"]["dni"];
      row += "," + data[i]["type"];
      csvString += row + "\n";
    }

    $scope.openFile(csvString);
  }

  $scope.openFile = function(csvString) {
    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:application/csv;charset=utf-8,' + encodeURIComponent(csvString));
    pom.setAttribute('download', "tutoria.csv");

    if (document.createEvent) {
      var event = document.createEvent('MouseEvents');
      event.initEvent('click', true, true);
      pom.dispatchEvent(event);
    } else {
      pom.click();
    }
  }

});

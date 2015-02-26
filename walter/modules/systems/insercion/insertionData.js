
var app = angular.module('mainApp');

app.controller('LaboralInsertionDataCtrl', function($scope, $timeout, LaboralInsertion) {

  $scope.addCv = function() {

//    $scope.$apply(function() {

      var f = document.getElementById('fileCv').files[0];
      var r = new FileReader();
      r.onloadend = function(e) {
        var data = e.target.result;
        // aca se tiene data con los datos del cv.

        var uInt8 = new Uint8Array(data);
        var len = uInt8.byteLength;
        var binary = '';
        for (var i = 0; i < len; i++) {
          binary += String.fromCharCode(uInt8[i]);
        }
        $scope.insertionData.cv = window.btoa(binary);
      }
      r.readAsArrayBuffer(f);

//    });

  }


  $scope.loadData = function() {

    LaboralInsertion.findLaboralInsertionData($scope.selectedUser,
      function(data) {
        $scope.insertionData = data;
      },
      function(err) {
        alert(err);
      });

  }

  $scope.$on('UpdateUserDataEvent',function(event,data) {
    $scope.loadData();
  });


  $timeout(function() {
    $scope.loadData();
  });


});

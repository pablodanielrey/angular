
var app = angular.module('mainApp');

app.controller('LaboralInsertionDataCtrl', function($scope) {

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

});

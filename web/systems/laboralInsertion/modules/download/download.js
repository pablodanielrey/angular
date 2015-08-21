angular
  .module('mainApp')
  .controller('DownloadCtrl',DownloadCtrl);

DownloadCtrl.$inject = ['$rootScope','$scope','$location', '$window', 'Notifications','LaboralInsertion', 'Utils'];

function DownloadCtrl($rootScope, $scope, $location, $window, Notifications, LaboralInsertion, Utils) {

    var vm = this;

    $scope.model = {
      message: '',
      fileToDownload: ''
    };

    $scope.initialize = function() {
      $scope.model.message = 'Obteniendo Datos Del Servidor';
      $scope.model.fileToDownload = '';
      LaboralInsertion.downloadDatabase(
        function(database) {
          $scope.model.message = 'Redirigiendo';
          //$window.open("http://" + window.location.hostname + "/d/" + database, '_blank');
          $scope.model.fileToDownload = "http://" + window.location.hostname + "/d/" + database;
          $scope.model.message = '';
          /*
          $scope.model.message = 'Convirtiendo a Formato de Archivo';
          var blob = Utils.base64ToBlob(database64);
          $scope.model.message = 'Guardando archivo';
          window.saveAs(blob,'base.zip');
          $scope.model.message = '';
          */

      }, function(err) {
          Notifications.message(err);
      });
    }

    $rootScope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });
}
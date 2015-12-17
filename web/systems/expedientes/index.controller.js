

app.controller('IndexCtrl',["$scope", "$timeout", "$modal", "$window", "Login", IndexCtrl]);

function IndexCtrl($scope, $timeout, $modal, $window, Login) {

  $scope.$on('$viewContentLoaded', function(event) {
     $scope.initialize();
  });

  $scope.initialize =  function() {

    if (!Login.isLogged()) {
      $window.location.href = "/systems/login/index.html";
    }
  }
  
  
  $scope.alerts = [];


  $scope.addAlert = function(newAlert) {
    
    for(var i = 0; i < $scope.alerts.length; i++){
      if(newAlert.msg == $scope.alerts[i].msg) return;
    }
    
    $scope.alerts.push(newAlert);
    
    var modalInstance = $modal.open({
      animation: true,
      templateUrl: "modalAlert.html",
      controller: "ModalAlertCtrl",
      size: "sm",
      resolve: {
        newAlert: function () { //"newAlert" debe coincidir con el nombre del servicio que se pasa al ModalCtrl
          return newAlert;
        }
      }
    });
    
    modalInstance.result.then(function (newAlert) {
      var index = $scope.alerts.indexOf(newAlert);
      $scope.alerts.splice(index, 1);
    }, function () {
      var index = $scope.alerts.indexOf(newAlert);
      $scope.alerts.splice(index, 1);
    });
    
    
    $timeout(function() { 
    
      modalInstance.close(newAlert);
    },5000);
  
  };
}

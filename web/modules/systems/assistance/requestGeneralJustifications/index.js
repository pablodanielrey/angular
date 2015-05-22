
app.controller('RequestGeneralJustificationsCtrl', ["$scope", "$timeout", "$window", "Assistance", "Module", "Notifications", "Users",  "Utils", function($scope, $timeout, $window, Assistance, Module, Notifications, Users, Utils) {

  /**
   * Variables del modelo en general
   */
  $scope.model = {
    sessionUserId: null, //id de sesion de usuario

    justificationsId: [],            //id de las justificaciones que el usuario tiene autorizadas
    justificationSelectedId: null,   //flag para indicar el id de la justificacion seleccionada si se debe mostrar la lista de usuarios

    //requestedJustifications
    requestedJustifications: [],    //justificaciones generales
    rjSort: ["dateSort", "justificationName"],       //ordenamiento de la lista de justificaciones
    rjReversed: false,   //flag para indicar el ordenamiento reverso de la lista de justificaciones
    loadRequestedJustifications: false  //flag para indicar que se esta procesando

  };



  /**************************************
   * METODOS DE REQUESTED JUSTIFICACION *
   **************************************/
  $scope.loadRequestedJustifications = function() {   
    $scope.model.loadRequestedJustifications = true;
    $scope.model.requestedJustifications = [];
    Assistance.getGeneralJustificationRequests(
      function(requestedJustifications) {
        for (var i = 0; i < requestedJustifications.length; i++) {
          var req = Utils.formatRequestJustification(requestedJustifications[i]);
          $scope.model.requestedJustifications.push(req);
        }
        
        $scope.model.loadRequestedJustifications = false;
      }, 
      function(error) {
        Notifications.message(error);
      }
    );
  };



  $scope.cancelRequest = function(request) {
    Assistance.deleteGeneralJustificationRequest(request.id,
      function(ok) {
        $scope.loadRequestedJustifications();
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };

  $scope.sortRequestedJustifications = function(sort){
    if($scope.model.rjSort[0] === sort){
      $scope.model.rjReversed = !$scope.model.rjReversed;
    } else {
      switch(sort){
        case "dateSort":
          $scope.model.rjSort = ["dateSort", "justificationName"]
        break;
        case "justificationName":
          $scope.model.rjSort = ["justificationName", "dateSort"]
        break;
        case "status":
          $scope.model.rjSort = ["status", "justificationName", "dateSort"]
        break;

      }
      $scope.model.rjReversed = false;
    }

  };


  
  /******************
   * INICIALIZACION *
   ******************/
  $timeout(function() {
    Module.authorize('ADMIN-ASSISTANCE,USER-ASSISTANCE',
      function(response){
        if (response !== 'granted') {
          Notifications.message("Acceso no autorizado");
          $window.location.href = "/#/logout";
        }
        $scope.model.sessionUserId = Module.getSessionUserId();
        $scope.loadRequestedJustifications();
      },
      function(error){
        Notifications.message(error);
        $window.location.href = "/#/logout";
      }
    );

    
  }, 0);


  $scope.$on('JustificationsRequestsUpdatedEvent', function(event, data){
    $scope.loadRequestedJustifications();

	});
  
  $scope.$on('JustificationsRequestsDeletedEvent', function(event, data){
    $scope.loadRequestedJustifications();

	});




}]);

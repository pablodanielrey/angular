

app.controller('NewRequestCtrl', ["$scope", "$timeout", "$window", "Module", "Notifications", "Issue", function ($scope, $timeout, $window, Module, Notifications, Issue) {
 
 
  $scope.data = [
  {
    "id": "sasdfiasdpfiasdfasdñfj",
    "title": "Reacondicionar oficina ",
    "nodes": [],
    "expanded":false
  },
  {
    "id": "sasdfiasdpfiasdddasdñfj",
    "title": "No se puede porque la puerta esta cerrada porque se rompio la cerradura y no hay forma de arreglarla así",
    "expanded":false,
    "nodes": [
      {
        "id": "212342342343",
        "title": "2.1. tofu-animation",
        "expanded":false,
        "nodes": [
          {
            "id": 211,
            "title": "2.1.1. spooky-giraffe",
            "expanded":false,
            "nodes": []
            
          },
          {
            "id": 212,
            "title": "2.1.2. bubble-burst",
            "expanded":false,
            "nodes": []
          }
        ]
      },
      {
        "id": 22,
        "title": "2.2. barehand-atomsplitting",
        "expanded":false,
        "nodes": []
      }
    ]
  },
  {
    "id": 3,
    "title": "3. unicorn-zapper",
    "expanded":false,
    "nodes": []
  },
  {
    "id": 4,
    "title": "4. romantic-transclusion",
    "expanded":false,
    "nodes": []
  }
];


  $scope.expandInput = function(model){
      var nodeData = model.$modelValue;
      nodeData.expanded = !nodeData.expanded ;
  };
  
  $scope.toggleItem = function (model) {
    model.toggle();
  };

  $scope.newSubItem = function(model) {
    model.expand();
    var nodeData = model.$modelValue;
    nodeData.nodes.push({
      "id": (nodeData["id"]+1),
      "title": "new" + (nodeData["id"]+1),
      "nodes": []
    });
  };

  
    

  $scope.request = {
    id: null,
    request: null,
    created: new Date(),
    requestorId: null,
    officeId: "8407abb2-33c2-46e7-bef6-d00bab573306",
    relatedRequestId:null,
    priority:null,
    visibility:null
  };
  
  /*$scope.requestState = {
    created: new Date(),
    state: "PENDING",
    request_id:null,
    user_id:$scope.global.sessionUserId,
  };*/
  
  $scope.errors = {
    request: null
  };
  
  
  $scope.checkRequest = function(){
    $scope.errors.request = null;
    if(!$scope.request.request) $scope.errors.request =  'No puede estar vacío';
  };
  
  
  
  
  /**
   * Enviar formulario
   * @returns {undefined}
   */
  $scope.submit = function(){
    $scope.checkRequest();
    for(var i in $scope.errors){
      if($scope.errors[i] !== null){
        Notifications.message("Verifique los datos del formulario");
        return;
      }
    }
    
    $scope.request.requestorId = $scope.global.sessionUserId;
    
    Issue.newRequest($scope.request,
      function(data) { Notifications.message("Registro agregado exitosamente"); },
      function(error) { Notifications.message(error); }
    );
    
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
        $scope.global.sessionUserId = Module.getSessionUserId();
      },
      function(error){
        Notifications.message(error);
        $window.location.href = "/#/logout";
      }
    );
  }, 0);
  
}]);

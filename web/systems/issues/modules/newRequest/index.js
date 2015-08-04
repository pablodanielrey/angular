
/**
 * Controlador asociado a la interfaz para agregar y visualizar issues
 * @param {type} param1
 * @param {type} param2
 */
app.controller('NewRequestCtrl', ["$scope", "$timeout", "$window", "Module", "Notifications", "Issue", "IssueClient", function ($scope, $timeout, $window, Module, Notifications, Issue, IssueClient) {

  $scope.request = null; //descripcion de un nuevo nodo que sera agregado a la raiz
  $scope.data = []; //todos los nodos
  
  /**
   * Inicializar nodo
   */
  $scope.initializeNode = function(){
    return {
      id: null,
      request: null,
      created: new Date(),
      requestorId: $scope.global.sessionUserId,
      officeId: "8407abb2-33c2-46e7-bef6-d00bab573306",
      relatedRequestId:null,
      priority:null,
      visibility:null
    };
  };
 

  $scope.expandInput = function(model){
      var nodeData = model.$modelValue;
      nodeData.expanded = !nodeData.expanded ;
  };

  $scope.expandDescription = function(model){
      var nodeData = model.$modelValue;
      nodeData.descriptionExpanded = !nodeData.descriptionExpanded ;
  };

  $scope.toggleItem = function (model) {
    model.toggle();
  };

  /*
  $scope.newSubItem = function(model) {
    model.expand();
    var nodeData = model.$modelValue;
    nodeData.nodes.push({
      "id": (nodeData["id"]+1),
      "title": "new" + (nodeData["id"]+1),
      "nodes": [],
      "expanded":false,
      "descriptionExpanded":false
    });
  };*/
  
  
  $scope.addNode = function(model){
    var nodeData = model.$modelValue;

    var newNode = $scope.initializeNode();
    newNode.relatedRequestId = nodeData.id;

    Issue.newRequest(newNode,
      function(data) { },
      function(error) { Notifications.message(error); }
    );
  };
  
  
  $scope.createNode = function(){
    var newNode = $scope.initializeNode();
    newNode.request = $scope.request;
 
    Issue.newRequest(newNode,
      function(data) {$scope.request = null; },
      function(error) { Notifications.message(error); }
    );
  };
  
  
  $scope.deleteNode = function(model){
    var nodeData = model.$modelValue;
    Issue.deleteIssue(nodeData.id,
      function(data){ },
      function(error) { Notifications.message(error); }
    );
  };

  /*
  $scope.comment = function(model) {
    model.expand();
    var nodeData = model.$modelValue;
    nodeData.nodes.push({
      "id": (nodeData["id"]+1),
      "title": "comentario",
      "nodes": [],
      "expanded":false,
      "descriptionExpanded":false
    });
  };*/

  /*$scope.requestState = {
    created: new Date(),
    state: "PENDING",
    request_id:null,
    user_id:$scope.global.sessionUserId,
  };*/



  /**
   * IssueDeletedEvent
   */
  $scope.$on('IssueInsertedEvent', function(event, node) { 
    if(node.relatedRequestId){
      IssueClient.addChild($scope.data, node);
    } else {
      $scope.data.push(node);
    }
  });
  

  
  /**
   * IssueDeletedEvent
   */
  $scope.$on('IssueDeletedEvent', function(event, id) {    
    IssueClient.deleteNode($scope.data, id);
  });




  /**
   * Obtener lista de tareas
   */
  $scope.getIssues = function(){
    Issue.getIssuesByUser($scope.global.sessionUserId,
      function(data) {
        $scope.data = IssueClient.generateTree(data);
      },
      function(error) { 
        Notifications.message(error); 
      }
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
        $scope.getIssues();
      },
      function(error){
        Notifications.message(error);
        $window.location.href = "/#/logout";
      }
    );
  
  
  }, 0);

}]);

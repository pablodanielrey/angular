
/**
 * Controlador asociado a la interfaz para agregar y visualizar issues
 * @param {type} param1
 * @param {type} param2
 */
app.controller('NewRequestCtrl', ["$scope", "$timeout", "$window", "Module", "Notifications", "Issue", "IssueClient", "Users", function ($scope, $timeout, $window, Module, Notifications, Issue, IssueClient, Users) {

  /***** MANIPULACION DE ESTILOS ******/
  $scope.style = null;
  $scope.styles = [];
  
  $scope.setStyle = function($index) {
    $scope.style = $scope.styles[$index];
  };


  $scope.request = null; //descripcion de un nuevo nodo que sera agregado a la raiz
  $scope.data = []; //raiz del arbol de nodos
  

    

 
  /**
   * Incrementar espacio de la descripcion del nodo al hacer click (textarea) para facilitar el ingreso de datos
   * @param {scope del nodo} nodeScope
   */
  $scope.expandTextarea = function(nodeScope){
      var nodeData = nodeScope.$modelValue;
      nodeData.expanded = !nodeData.expanded ;
  };
  
  
  
  /**
   * Interruptor para visualizar subnodos
   * @param {type} nodeScope
   */
  $scope.toggleNode = function (nodeScope) {
    nodeScope.toggle();
  };
  
  
  
  /**
   * Interruptor para visualizar descripcion del nodo
   * @param {type} nodeScope
   */
  $scope.toggleNodeData = function (nodeScope) {
    var nodeData = nodeScope.$modelValue;
    nodeData.collapsedDescription = !nodeData.collapsedDescription
  };
  
  
  

  $scope.expandDescription = function(nodeScope){
    var nodeData = nodeScope.$modelValue;
    nodeData.descriptionExpanded = !nodeData.descriptionExpanded ;
  };


  /**
   * Actualizar los datos de un nodo (solo se actualizan los datos y no la posicion en el arbol)
   * @param {type} nodeScope
   * @returns {undefined}
   */
  $scope.updateIssueData = function(nodeScope){
    
    var nodeData = nodeScope.$modelValue;
    Issue.updateIssueData(nodeData, $scope.global.sessionUserId,
      function(data) { },
      function(error) { Notifications.message(error); }
    );
  };
  

  
  $scope.addNode = function(nodeScope){
    var nodeData = nodeScope.$modelValue;

    var newNode = IssueClient.initializeNode($scope.global.sessionUserId, "PENDING");
    newNode.relatedRequestId = nodeData.id;

    Issue.newRequest(newNode,
      function(data) { },
      function(error) { Notifications.message(error); }
    );
  };
  
  $scope.addComment = function(nodeScope){
    var nodeData = nodeScope.$modelValue;

    var newNode = IssueClient.initializeNode($scope.global.sessionUserId, "COMMENT");
    newNode.relatedRequestId = nodeData.id;
    console.log(newNode);

    Issue.newRequest(newNode,
      function(data) { },
      function(error) { Notifications.message(error); }
    );
  };
  
  
  
  
  $scope.createNode = function(){
    var newNode = IssueClient.initializeNode($scope.global.sessionUserId, "PENDING");
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

 


  /**
   * IssueDeletedEvent
   */
  $scope.$on('IssueInsertedEvent', function(event, node) { 
    IssueClient.addChild($scope.data, node);

    

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

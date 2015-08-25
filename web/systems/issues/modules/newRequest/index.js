
/**
 * Controlador asociado a la interfaz para agregar y visualizar issues
 * @param {type} param1
 * @param {type} param2
 */
app.controller('NewRequestCtrl', ["$scope", "$timeout", "$window", "Module", "Notifications", "Issue", "Users", function ($scope, $timeout, $window, Module, Notifications, Issue, Users) {

  /***** MANIPULACION DE ESTILOS ******/
  $scope.style = null;
  $scope.styles = [];

  $scope.setStyle = function($index) {
    $scope.style = $scope.styles[$index];
  };

  $scope.setNodeStyleByState = function(state) {
     switch(state){
      case "COMMENT": return "commentOrder";
      default: return "normal";

    }
  };


  /***** ATRIBUTOS ******/
  $scope.request = null; //descripcion de un nuevo nodo que sera agregado a la raiz
  $scope.data = []; //raiz del arbol de nodos




  /**
   * Inicializar nodo con valores por defecto. Cuando se crea un nuevo nodo en el arbol se inicializa y guarda en la base con los siguientes parametros
   */
  $scope.initializeNode = function(status){
    return {
      id: null,
      request: null,
      created: new Date(),
      requestorId: null,
      office_id: "8407abb2-33c2-46e7-bef6-d00bab573306",
      relatedRequestId:null,
      priority:null,
      collapsedDescription: false,
      state: status,
      style: $scope.setNodeStyleByState(status)
    };
  };



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
    Issue.updateIssueData(nodeData, null,
      function(data) {$scope.getIssues();},
      function(error) { Notifications.message(error); }
    );
  };



  $scope.addNode = function(nodeScope){
    var nodeData = nodeScope.$modelValue;

    var newNode = $scope.initializeNode("PENDING");
    newNode.parent_id = nodeData.id;
    newNode.request = $scope.request;
    newNode.visibilities = []

    Issue.newIssue(newNode,newNode['state'], newNode['visibilities'],
      function(data) {$scope.getIssues(); $scope.request = null;},
      function(error) { Notifications.message(error); }
    );
  };

  $scope.addComment = function(nodeScope){
    var nodeData = nodeScope.$modelValue;

    var newNode = $scope.initializeNode("COMMENT");
    newNode.parent_id = nodeData.id;
    newNode.request = $scope.request;
    newNode.visibilities = []

    Issue.newIssue(newNode,newNode['state'],newNode['visibilities'],
      function(data) {
        $scope.getIssues();
        $scope.request = null;
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };




  $scope.createNode = function(){
    var newNode = $scope.initializeNode("PENDING");
    newNode.request = $scope.request;
    newNode.visibilities = []

    Issue.newIssue(newNode,newNode['state'],newNode['visibilities'],
      function(data) {$scope.getIssues();$scope.request = null; },
      function(error) { Notifications.message(error); }
    );
  };


  $scope.deleteNode = function(model){
    var nodeData = model.$modelValue;
    Issue.deleteIssue(nodeData.id,
      function(data){ $scope.getIssues();},
      function(error) { Notifications.message(error); }
    );
  };




  /**
   * Obtener lista de tareas
   */
  $scope.getIssues = function(){
    Issue.getIssues(null,
      function(data) {
        $scope.data = data;
        for (var i = 0; i< data.length; i++) {
          $scope.loadDataNode(data[i]);
        }
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };



  $scope.loadDataNode = function(node) {
    Users.findUser(node.requestor_id,
      function(user) {
        node.requestor = user.name + " " + user.lastname;
      },
      function(error) {
      }
    );

    node.collapsedDescription = false;
    node.style = $scope.setNodeStyleByState(node.state);
    for (var i = 0; i < node.childrens.length; i++) {
      $scope.loadDataNode(node.childrens[i]);
    }
  }






  /*
    ABRIR LA PANTALLA DE VISIBILIDAD DE GRUPO
  */
  $scope.openVisibility = openVisibility;
  function openVisibility(issue) {
      console.log('open visibility');
  }


  /******************
   * INICIALIZACION *
   ******************/

  $scope.$on('$viewContentLoaded', function(event) {
   $scope.initialize();
  });

  $scope.initialize = initialize;
  function initialize() {
    $scope.getIssues();
  }

}]);

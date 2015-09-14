
/**
 * Controlador asociado a la interfaz para agregar y visualizar issues
 * @param {type} param1
 * @param {type} param2
 */
app.controller('NewRequestCtrl', ["$scope", "$timeout", "$window", "Module", "Notifications", "Issue", "Users", function ($scope, $timeout, $window, Module, Notifications, Issue, Users) {

  /***** MANIPULACION DE ESTILOS ******/
  $scope.style = null;
  $scope.styles = ['none','displayVisibility','displayCreateChild'];

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
  $scope.model = {
    newNode: null
  }

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
  $scope.toggleNodeData = function (node) {
    node.descriptionExpanded = !node.descriptionExpanded;
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
  $scope.updateIssueData = function(nodeData){
    Issue.updateIssueData(nodeData, null,
      function(data) {$scope.getIssues();},
      function(error) { Notifications.message(error); }
    );
  };



  $scope.addNode = function(nodeData){
    $scope.requestNewNode = "";
    $scope.setStyle(2);

    $scope.model.newNode = $scope.initializeNode("PENDING");
    $scope.model.newNode.parent_id = nodeData.id;
    $scope.model.newNode.request = $scope.request;
    $scope.model.newNode.visibilities = nodeData['visibilities'];
  };

  $scope.addComment = function(nodeData){
    $scope.requestNewNode = "";
    $scope.setStyle(2);

    $scope.model.newNode = $scope.initializeNode("COMMENT");
    $scope.model.newNode.parent_id = nodeData.id;
    $scope.model.newNode.request = $scope.request;
    $scope.model.newNode.visibilities = nodeData['visibilities'];
  };


  $scope.saveChild = function() {
    $scope.model.newNode.request = $scope.requestNewNode;
    Issue.newIssue($scope.model.newNode,$scope.model.newNode['state'],$scope.model.newNode['visibilities'],
      function(data) {
        $scope.setStyle(0);
        $scope.getIssues();
        $scope.request = null;
      },
      function(error) {
        $scope.setStyle(0);
        Notifications.message(error);
      }
    );
  }

  $scope.cancelChild = function() {
    $scope.setStyle(0);
  }

  $scope.createNode = function(){
    var newNode = $scope.initializeNode("PENDING");
    newNode.request = $scope.request;
    off = $scope.model.offices[0];
    newNode.visibilities = [{'office_id':off.id,'tree':false,'type':'OFFICE'}]

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
    console.log(node);
    Users.findUser(node.creator,
      function(user) {
        node.requestor = user.name + " " + user.lastname;
      },
      function(error) {
      }
    );

    node.collapsedDescription = false;
    node.descriptionExpanded = false;
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
    $scope.$broadcast('displayVisbilityEvent',issue);
    $scope.setStyle(1);
  }


  /******************
   * INICIALIZACION *
   ******************/

  $scope.$on('$viewContentLoaded', function(event) {
   $scope.initialize();
  });

  $scope.$on('saveVisibilityEvent', function(event,issue,selecteds) {
    $scope.setStyle(0);
    issue.visibilities = selecteds;
    Issue.updateIssueData(issue, null,
      function(response) {
        $scope.getIssues();
      },
      function(error) {
        Notifications.message(error);
      }
    );
  });

  $scope.$on('cancelVisibilityEvent', function(event) {
    $scope.setStyle(0);
  });

  $scope.initialize = initialize;
  function initialize() {
    $scope.model.newNode = null;
    $scope.getIssues();
  }

}]);

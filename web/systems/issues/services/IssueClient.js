
/**
 * Metodos de uso general para visualizar y reorganizar el arbol de nodos de Issue
 * @param {type} param1
 * @param {type} param2
 */
app.service('IssueClient', ["Users", "Utils", function(Users, Utils) {


  this.defineStyle = function(state){
     switch(state){
      case "COMMENT": return "commentOrder";
      default: return "normal";

    }
  };

  /**
   * Inicializar nodo. Cuando se crea un nuevo nodo en el arbol se inicializa y guarda en la base con los siguientes parametros
   */
  this.initializeNode = function(status){
    var style = this.defineStyle(status);

    return {
      id: null,
      request: null,
      created: new Date(),
      requestorId: null,
      office_id: "8407abb2-33c2-46e7-bef6-d00bab573306",
      relatedRequestId:null,
      priority:null,
      visibility:null,
      collapsedDescription: false,
      state: status,
      style: style
    };
  };


  this.loadDataNode = function(node) {
    Users.findUser(node.requestor_id,
      function(user) {
        node.requestor = user.name + " " + user.lastname;
      },
      function(error) {
      }
    );

    node.collapsedDescription = false;
    node.style = this.defineStyle(node.state);
    for (var i = 0; i < node.childrens.length; i++) {
      this.loadDataNode(node.childrens[i]);
    }
  }

  /**
   * Generar arbol de pedidos
   * @param {Object} request Datos del pedido
   * @param {function} callbackOk
   * @param {function} callbackError
   */
  this.generateTree = function(data) {
    var issues = [];
    for(var i in data){

      Users.findUser(data[i].requestor_id,
        function(response){ data[i].requestor = response.name + " " + response.lastname; },
        function(error){ console.log(error); }
      );

      data[i].collapsedDescription = false;
      data[i].style = this.defineStyle(data[i].state);

      if(!("nodes" in data[i])) data[i]["nodes"] = [];
      var assigned = false;

      if(data[i].related_request_id != null){
        for(var j in data){
          if(data[j].id == data[i].related_request_id){
            if(!("nodes" in data[j])) data[j]["nodes"] = [];
            data[j]["nodes"].push(data[i]);
            assigned = true;
          }
        }
      }

      if(!assigned){
        issues.push(data[i]);
      }
    }

    return issues;
  };



  /**
   * Agregar nodo
   * @param {type} data
   * @param {type} node
   * @returns {Boolean}
   */
  this.addChild = function(data, node){
    var newNode = this.initializeNode(node.requestorId, node.state);

    Utils.joinObjects(node, newNode);

    if(!node.relatedRequestId){
      data.push(node);
      return true;
    }

    //var nodeAux = this.initializeNode(node)
    for(var i in data){
      if(data[i].id == node.relatedRequestId) {
        data[i].nodes.push(node);
        return true;
      }

      if((("nodes" in data[i])) && (data[i]["nodes"].length > 0)){
        var add = this.addChild(data[i]["nodes"], node);
        if(add) return true;
      }
    }

    return false;

  };

  /**
   * Eliminar nodo
   * @param {type} data
   * @param {type} node
   * @returns {undefined}
   */
  this.deleteNode = function(data, id){

    for(var i in data){
      if(data[i].id == id) {
        data.splice(i, 1);
        return true;
      }

      if((("nodes" in data[i])) && (data[i]["nodes"].length > 0)){
        var add = this.deleteNode(data[i]["nodes"], id);
        if(add) return true;
      }
    }

    return false;
  };

}]);
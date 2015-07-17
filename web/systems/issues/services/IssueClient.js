

app.service('IssueClient', [function() {
	
  
  /**
   * Generar arbol de pedidos
   * @param {Object} request Datos del pedido
   * @param {function} callbackOk
   * @param {function} callbackError
   */
  this.generateTree = function(data) {
    
    var issues = [];
    for(var i in data){
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
  
  
  
  
  this.addChild = function(data, node){
  
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
  
  
  this.deleteNode = function(data, node){
    for(var i in data){
      if((("nodes" in data[i])) && (data[i]["nodes"].length > 0)){
      
      }
    }
    
  }

}]);

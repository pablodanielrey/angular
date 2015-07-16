

app.service('IssueClient', ['Utils','Messages','Session', function(Utils,Messages,Session) {
	
  
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
  
  
  this.deleteIssue = function (id, tree){
    
    
  }
  
  
  



}]);

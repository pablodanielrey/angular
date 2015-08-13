

app.service('Issue', ['Utils','Messages','Session', function(Utils,Messages,Session) {
	
  /**
   * Solicitar un nuevo pedido
   * @param {Object} request Datos del pedido
   * @param {function} callbackOk
   * @param {function} callbackError
   */
  this.newRequest = function(request, callbackOk, callbackError) {
    
  
    
    var msg = {
      id: Utils.getId(),
      action: 'newIssueRequest',
      session: Session.getSessionId(),
      request: request
    };


    Messages.send(msg,
      function(data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.response);
        } else {
          callbackError(data.error);
        }
      });
  };
  
  
  /**
   * Retornar todas las issues solicitadas por el usuario o aquellas cuyo responsable es el usuario
   * @param {type} userId
   * @param {type} callbackOk
   * @param {type} callbackError
   * @returns {undefined}
   */
  this.getIssuesByUser = function (userId, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      action: 'getIssuesByUser',
      session: Session.getSessionId(),
      request: {
        userId: userId
      }
    };

    Messages.send(msg,
      function (data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.response);
        } else {
          callbackError(data.error);
        }
    });
  };
  
  
  
  /**
   * Retornar todas las issues solicitadas por el usuario o aquellas cuyo responsable es el usuario
   * @param {type} userId
   * @param {type} callbackOk
   * @param {type} callbackError
   * @returns {undefined}
   */
  this.getIssues = function (userId, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      action: 'getIssues',
      session: Session.getSessionId(),
      request: {
        userId: userId
      }
    };

    Messages.send(msg,
      function (data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.response);
        } else {
          callbackError(data.error);
        }
    });
  };
  
  
  
  
  /**
   * Elimina el arbol de nodos a partir del nodo id
   * @param {type} id
   * @param {type} callbackOk
   * @param {type} callbackError
   * @returns {undefined}
   */
  this.deleteIssue = function(id, callbackOk, callbackError){
    var msg = {
      id: Utils.getId(),
      action: 'deleteIssue',
      session: Session.getSessionId(),
      request: {
        id: id
      }
    };

    Messages.send(msg,
      function (data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.response);
        } else {
          callbackError(data.error);
        }
    });
  };
  
  
  
  
  
  /**
   * @param {type} issue Datos del issue
   * @param {type} userId Id del usuario que solicita la actualizacion de datos (quiza sea alguien diferente a quien solicito el issue)
   * @param {type} callbackOk
   * @param {type} callbackError
   * @returns {undefined}
   */
  this.updateIssueData = function(issue, userId, callbackOk, callbackError){
    var msg = {
      id: Utils.getId(),
      action: 'updateIssueData',
      session: Session.getSessionId(),
      issue: issue,
      userId: userId
    };
    
    Messages.send(msg,
      function (data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.response);
        } else {
          callbackError(data.error);
        }
    });
    
  };
  
  
}]);



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


  console.log(msg);
    Messages.send(msg,
      function(data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.response);
        } else {
          callbackError(data.error);
        }
      });
  };


}]);

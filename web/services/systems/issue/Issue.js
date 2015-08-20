angular
  .module('mainApp')
  .service('Issue',Issue);

Issue.inject = ['$rootScope','$wamp','Session']

function Issue($rootScope,$wamp,Session) {

  var services = this;

  // Crea una nueva tarea
  services.newIssue = newIssue;
  // Retornar todas las issues solicitadas por el usuario o aquellas cuyo responsable es el usuario
  services.getIssues = getIssues;
  // elimina el pedido y sus hijos
  services.deleteIssue = deleteIssue;
  //  actualizacion de los datos del issue.
  services.updateIssueData = updateIssueData;

  // Crea una nueva tarea
  function newIssue(issue, callbackOk, callbackError) {
    $wamp.call('issue.issue.newIssue', [issue])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError('Error');
    });
  }

  // Retorna todas las issues solicitadas por el usuario o aquellas cuyo responsable es el usuario
  // si el userId es null tomo por defecto el id del usuario logueado
  function getIssues(userId, callbackOk, callbackError) {
    $wamp.call('issue.issue.getIssues', [userId])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError('Error');
    });
  }

  // elimina el pedido y sus hijos
  function deleteIssue(id, callbackOk, callbackError) {
    $wamp.call('issue.issue.deleteIssue', [id])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError('Error');
    });
  }

  // Actualiza los datos del issue
  // userId Id del usuario que solicita la actualizacion de datos (quiza sea alguien diferente a quien solicito el issue)
  function updateIssueData(issuer, userId, callbackOk, callbackError) {
    $wamp.call('issue.issue.updateIssueData', [issuer,userId])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError('Error');
    });
  }

}

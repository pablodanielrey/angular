angular
  .module('mainApp')
  .service('Issue',Issue);

Issue.inject = ['$rootScope','$wamp','Session']

function Issue($rootScope,$wamp,Session) {

  var services = this;

  // Crea una nueva tarea
  services.newIssue = newIssue;


  function newIssue(issue, callbackOk,callbackError) {
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
}

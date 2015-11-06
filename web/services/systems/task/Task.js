angular
  .module('mainApp')
  .service('Task',Task);

Task.inject = ['$rootScope','$wamp','Session']

function Task($rootScope,$wamp,Session) {

  var services = this;

  
  // otiene las tareas del usuario logueado
  services.getTasks = getTasks;
  
  // crea una nueva tarea
  services.createTask = createTask;
  
  // actualiza el estado de la tarea
  services.updateStatus = updateStatus;
  
  // elimina una tarea
  services.removeTask = removeTask;
  
  // elimina todas las tareas que esten finalizadas
  services.removeTaskByStatus = removeTaskByStatus;
  

  
  /*
    res = [{
	    text:contenido de la tarea,
	    finish:boolean,
	    id:1,
	    created: fecha de creacion    
	  }]
   */
  function getTasks(callbackOk,callbackError) {
    sessionId = Session.getSessionId();
     $wamp.call('task.getTasks', [sessionId])
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
  
  function createTask(text,callbackOk,callbackError) {
    sessionId = Session.getSessionId();
     $wamp.call('task.createTask', [sessionId,text])
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
  
  
  function updateStatus(taskId,status,callbackOk,callbackError) {
    sessionId = Session.getSessionId();
     $wamp.call('task.updateStatus', [sessionId,taskId,status])
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
  
  function removeTask(taskId,callbackOk,callbackError) {
    sessionId = Session.getSessionId();
     $wamp.call('task.removeTask', [sessionId,taskId])
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
  
  function removeTaskByStatus(status,callbackOk,callbackError) {
    sessionId = Session.getSessionId();
     $wamp.call('task.removeTaskByStatus', [sessionId,status])
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

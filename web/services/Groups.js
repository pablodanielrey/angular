
var app = angular.module('mainApp');

app.service('Groups', function($rootScope, Messages, Session, Utils, Cache, Config) {


  this.addMembers = function(id, members, ok, err) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'addMembers',
      group: {
        id: id,
        members: members
      }
    };
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        err(response.error);
      } else {
        ok(response.ok);
      }
    });
  }


  this.removeMembers = function(id, members, ok, err) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'removeMembers',
      group: {
        id: id,
        members: members
      }
    };
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        err(response.error);
      } else {
        ok(response.ok);
      }
    });
  }


  this.findMembers = function(id, ok, err) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'findMembers',
      group: { id: id }
    };
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        err(response.error);
      } else {
        ok(response.group.members);
      }
    })
  }


  // obtiene los datos de un usuario cuyo id es el pasado por parámetro.
  this.findGroup = function(id, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'findGroup',
      group: { id: id }
    }
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.group);
      }
    });
  }


  this.createGroup = function(group, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'createGroup',
      group: group
    };
    Messages.send(msg,function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.ok);
      }
    });
  }

  this.updateGroup = function(group, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'updateGroup',
      group: group
    };
    Messages.send(msg,function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.ok);
      }
    });
  }


  this.listGroups = function(callbackOk, callbackError) {
    var  msg = {
      id: Utils.getId(),
      action: 'listGroups',
      session: Session.getSessionId(),
    };
    Messages.send(msg, function(response) {
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.groups);
      }
    });
  }

});

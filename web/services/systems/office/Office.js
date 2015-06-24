angular
    .module('mainApp')
    .service('Office', Office);

Office.$inject = ['$rootScope', 'Messages', 'Session', 'Utils', 'Cache', 'Config'];

function Office($rootScope, Messages, Session, Utils, Cache, Config) {

  var services = this;

  services.getUserInOfficesByRole = getUserInOfficesByRole;
  services.getUserOfficeRoles = getUserOfficeRoles;
  services.getOffices = getOffices;
  services.getOfficesByUserRole = getOfficesByUserRole;
  services.getOfficesUsers = getOfficesUsers;
  services.deleteOfficeRole = deleteOfficeRole;
  services.addOfficeRole = addOfficeRole;
  services.persistOffice = persistOffice;
  services.removeUserFromOffice = removeUserFromOffice;
  services.addUserToOffices = addUserToOffices;

  function getUserInOfficesByRole(userId, role, tree, callbackOk, callbackError) {
    if (role == null) {
      return;
    }

    if (tree == null) {
      tree = true;
    }

    var msg = {
      id: Utils.getId(),
      action: 'getUserInOfficesByRole',
      session: Session.getSessionId(),
      request: {
        tree: tree,
        role: role
      }
    }

    if (userId != null) {
      msg.request.userId = userId;
    }

    Messages.send(msg,
      function(data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.response.users);
        } else {
          callbackError(data.error);
        }
      });

  }

  function getUserOfficeRoles() {}

  function getOffices(userId, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      action: 'getOffices',
      session: Session.getSessionId(),
      request:{}
    }

    if (userId != null) {
      msg.request.user_id = userId;
    }

    Messages.send(msg,
      function(data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.response.offices);
        } else {
          callbackError(data.error);
        }
    });

  }

  function getOfficesByUserRole(userId,role,tree, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      action: 'getOfficesByUserRole',
      session: Session.getSessionId(),
      request:{
        user_id: userId,
        tree:tree
      }
    }

    if (role != null) {
      msg.request.role = role;
    }

    Messages.send(msg,
      function(data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.response.offices);
        } else {
          callbackError(data.error);
        }
    });
  }

  /*
  Obtiene todos los usuarios de las oficinas pasadas como parametro
  */
  function getOfficesUsers(offices, callbackOk, callbackError) {
    var msg = {
      id: Utils.getId(),
      action: 'getOfficesUsers',
      session: Session.getSessionId(),
      request: {
        offices: offices
      }
    }

    Messages.send(msg,
      function(data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.response.users);
        } else {
          callbackError(data.error);
        }
      });
  }

  function deleteOfficeRole() {}

  function addOfficeRole() {}

  function persistOffice(office, callbackOk, callbackError) {
    if (office == null) {
      return;
    }

    if (office.name == null || office.name.trim() == '') {
      return;
    }

    var msg = {
      id: Utils.getId(),
      action: 'persistOffice',
      session: Session.getSessionId(),
      request: {
        office: {}
      }
    }

    msg.request.office.name = office.name;

    if (office.telephone != null && office.telephone.trim() != '') {
      msg.request.office.telephone = office.telephone;
    }

    if (office.email != null && office.email.trim() != '') {
      msg.request.office.email = office.email;
    }

    if (office.parent != null && office.parent.trim() != '') {
      msg.request.office.parent = office.parent;
    }

    if (office.id != null) {
      msg.request.office.id = office.id;
    }

    Messages.send(msg,
      function(data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.ok);
        } else {
          callbackError(data.error);
        }
      });
  }

  function removeUserFromOffice(userId, officeId, callbackOk,callbackError) {
    if (userId == null || officeId == null) {
        return;
    }

    var msg = {
      id: Utils.getId(),
      action: 'removeUserFromOffice',
      session: Session.getSessionId(),
      request: {
        userId: userId,
        officeId: officeId
      }
    }

    Messages.send(msg,
      function(data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.ok);
        } else {
          callbackError(data.error);
        }
    });

  }

  function addUserToOffices(userId, officeId, callbackOk,callbackError) {
    if (userId == null || officeId == null) {
        return;
    }

    var msg = {
      id: Utils.getId(),
      action: 'addUserToOffices',
      session: Session.getSessionId(),
      request: {
        userId: userId,
        officeId: officeId
      }
    }

    Messages.send(msg,
      function(data) {
        if (typeof data.error === 'undefined') {
          callbackOk(data.ok);
        } else {
          callbackError(data.error);
        }
    });
  }
}

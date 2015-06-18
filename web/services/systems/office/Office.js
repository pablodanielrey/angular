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

  function getUserInOfficesByRole() {}

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

  function getOfficesByUserRole() {}

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

  function persistOffice() {}

  function removeUserFromOffice() {}

  function addUserToOffices() {}
}

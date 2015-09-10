angular
  .module('mainApp')
  .service('Office',Office);

Office.inject = ['$rootScope','$wamp','Session'];

function Office($rootScope, $wamp, Session) {

  var services = this;

  //retorna todas las oficinas
  services.getOffices = getOffices;

  //retorna todas las oficinas en forma de arbol
  services.getOfficesTree = getOfficesTree;

  // obtiene las oficinas que puede ver el usuario
  services.getOfficesByUser = getOfficesByUser;

  // obtiene las oficinas que puede ver el usuario en forma de arbol
  services.getOfficesTreeByUser = getOfficesTreeByUser;

  // obtiene todos los usuarios de las oficinas pasadas como parametro
  services.getOfficesUsers = getOfficesUsers;

  // retorna los usuarios que pertenecen a las oficinas y suboficinas en las cuales la persona userId tiene un rol determinado
  services.getUserInOfficesByRole = getUserInOfficesByRole;

  // obtiene todas las oficinas en las cuales el usuario tiene asignado un rol
  services.getOfficesByUserRole = getOfficesByUserRole;

  // elimina el rol para usuario oficina
  services.deleteOfficeRole = deleteOfficeRole;


  // -----------------------------------------------------------
  // --------------- FALTAN IMPLEMENTAR EN EL SERVER -----------
  // -----------------------------------------------------------

  // setea el rol role al usuario userId para la oficina officeId
  services.addOfficeRole = addOfficeRole;

  // actualiza los roles para todos los usersId en officesId
  services.persistOfficeRole = persistOfficeRole;

  // crea una nueva oficina si no existe o sino actualiza los datos
  services.persistOffice = persistOffice;

  // elimina un usuario de una oficina
  services.removeUserFromOffice = removeUserFromOffice;

  // agrega un usuario (userId) a una oficina (officeId)
  services.addUserToOffices = addUserToOffices;

  // Retorna los roles que puede asignar el usuario (userId) para las oficinas (officesId) y para los usuarios (usersId)
  // Ademas retorna los roles que ya poseen los usarios
  services.getRolesAdmin = getRolesAdmin;



  /*
    obtiene todas las oficinas
    res = [{
            name:'',
            parent:'' -- id de la oficina padre,
            id:'',
            email:'',
            telephone:''
          }]
  */
  function getOffices(callbackOk,callbackError) {
    $wamp.call('offices.offices.getOffices', [])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError(err);
    });
  }


  /*
    obtiene todas las oficinas
    res = [{
            name:'',
            parent:'' -- id de la oficina padre,
            id:'',
            email:'',
            telephone:'',
            childrens: []
          }]
  */
  function getOfficesTree(callbackOk,callbackError) {
    $wamp.call('offices.offices.getOfficesTree', [])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError(err);
    });
  }
  /*
    obtiene las oficinas que puede ver el usuario
    res = [{
            name:'',
            parent:'' -- id de la oficina padre,
            id:'',
            email:'',
            telephone:''
          }]
  */
  function getOfficesByUser(userId,tree,callbackOk,callbackError) {
    sessionId = Session.getSessionId();
    $wamp.call('offices.offices.getOfficesByUser', [sessionId,userId,tree])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError(err);
    });
  }

  /*
    obtiene las oficinas que puede ver el usuario
    res = [{
            name:'',
            parent:'' -- id de la oficina padre,
            id:'',
            email:'',
            telephone:'',
            childrens:[]
          }]
  */
  function getOfficesTreeByUser(userId,callbackOk,callbackError) {
    sessionId = Session.getSessionId();
    $wamp.call('offices.offices.getOfficesTreeByUser', [sessionId,userId])
    .then(function(res) {
      if (res != null) {
        callbackOk(res);
      } else {
        callbackError('Error');
      }
    },function(err) {
      callbackError(err);
    });
  }

  /*
  Obtiene todos los usuarios de las oficinas pasadas como parametro
  */
  function getOfficesUsers(offices, callbackOk, callbackError) {
    $wamp.call('offices.offices.getOfficesUsers', [offices])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      },function(err) {
        callbackError(err);
      });
  }


  /*
    retorna los usuarios que pertenecen a las oficinas y suboficinas en las cuales la persona userId tiene un rol determinado
  */
  function getUserInOfficesByRole(userId, role, tree, callbackOk, callbackError) {
    if (role == null) {
      return;
    }

    $wamp.call('offices.offices.getUserInOfficesByRole', [userId,role,tree])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      },function(err) {
        callbackError(err);
      });
    }

  /*
  obtiene todas las oficinas en las cuales el usuario tiene asignado un rol
  si tree=True obtiene todas las hijas también
  */
  function getOfficesByUserRole(userId, role, tree, callbackOk, callbackError) {
    $wamp.call('offices.offices.getOfficesByUserRole', [userId,role,tree])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      },function(err) {
        callbackError(err);
      });
  }

  /*
  elimina el rol para usuario oficina
  */
  function deleteOfficeRole(officesId, usersId, role, callbackOk, callbackError) {
    if (officesId == null || usersId == null || role == null) {
      return;
    }
    $wamp.call('offices.offices.deleteOfficeRole', [officesId, usersId, role])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      },function(err) {
        callbackError(err);
      });
  }

  /*
    setea el rol role al usuario userId para la oficina officeId
  */
  function addOfficeRole(officesId, usersId, role, callbackOk, callbackError) {
    if (officesId == null || usersId == null || role == null) {
      return;
    }
    $wamp.call('offices.offices.addOfficeRole', [officesId, usersId, role])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      },function(err) {
        callbackError(err);
      });
  }

  /*
    actualiza los roles para todos los usersId en officesId
  */
  function persistOfficeRole(officesId, usersId, roles, oldRoles) {
    if (officesId == null || usersId == null || roles == null || oldRoles == null) {
      return;
    }
    $wamp.call('offices.offices.persistOfficeRole', [officesId, usersId, roles, oldRoles])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      },function(err) {
        callbackError(err);
      });
  }


  /*
    crea una nueva oficina si no existe o sino actualiza los datos
  */
  function persistOffice(office, callbackOk, callbackError) {
    if (office == null || office.name == null || office.name.trim() == '') {
      return;
    }

    sessionId = Session.getSessionId();
    $wamp.call('offices.offices.persistOffice', [sessionId,office])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      },function(err) {
        callbackError(err);
      });
  }

  /*
    elimina un usuario de una oficina
  */
  function removeUserFromOffice(userId, officeId, callbackOk,callbackError) {
    if (userId == null || officeId == null) {
        return;
    }
    $wamp.call('offices.offices.removeUserFromOffice', [userId, officeId])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      },function(err) {
        callbackError(err);
      });
  }

  /*
    agrega un usuario (userId) a una oficina (officeId)
  */
  function addUserToOffices(userId, officeId, callbackOk,callbackError) {
    if (userId == null || officeId == null) {
        return;
    }
    $wamp.call('offices.offices.addUserToOffices', [userId, officeId])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      },function(err) {
        callbackError(err);
      });
  }

  /*
    Retorna los roles que puede asignar el usuario (userId) para las oficinas (officesId) y para los usuarios (usersId)
    Ademas retorna los roles que ya poseen los usarios
  */
  function getRolesAdmin(userId, officesId, usersId, callbackOk, callbackError) {
    if (officesId == null || usersId == null) {
      return;
    }
    sessionId = Session.getSessionId();
    $wamp.call('offices.offices.getRolesAdmin', [sessionId, userId, officesId, usersId])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      },function(err) {
        callbackError(err);
      });
  }

}

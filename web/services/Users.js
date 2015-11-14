angular
  .module('mainApp')
  .service('Users',Users);

Users.inject = ['$rootScope', '$wamp', 'Session','Utils','Cache'];

function Users($rootScope, $wamp, Session, Utils, Cache) {

  var instance = this;
  this.userPrefix = 'user_';

  $rootScope.$on('UserUpdatedEvent', function(event,id) {
    Cache.removeItem(instance.userPrefix + id);
  });

    this.deleteMail = function(id, callbackOk, callbackError) {
      $wamp.call('users.mails.deleteMail', [id])
        .then(function(res) {
          if (res != null) {
            callbackOk(res);
          } else {
            callbackError('Error');
          }
        }, function(err) {
          callbackError(err);
        });
    }


  this.confirmMail = function(hash, callbackOk, callbackError) {
    $wamp.call('users.mails.confirmMail', [hash])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      }, function(err) {
        callbackError(err);
      });
  }



  /*
    Envía un mail de confirmación al email dado por mail_id
  */
  this.sendConfirmMail = function(id, callbackOk, callbackError) {
    $wamp.call('users.mails.sendConfirmMail', [id])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      }, function(err) {
        callbackError(err);
      });
  }

  this.addMail = function(userId, email, callbackOk, callbackError) {
    $wamp.call('users.mails.persistMail', [userId, email])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      }, function(err) {
        callbackError(err);
      });
  }

  this.findMails = function(userId, callbackOk, callbackError) {
    $wamp.call('users.mails.findMails', [userId])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      }, function(err) {
        callbackError(err);
      });
  }


  this.normalizeUser = function(user) {
    if (user.birthdate != undefined) {
      //user.birthdate = new Date(user.birthdate)
    }
  }





  this.findUser = function(id, callbackOk, callbackError) {

    // chequeo la cache primero
    //var user = Cache.getItem(instance.userPrefix + id);
    //if (user != null) {
    //  callbackOk(user);
    //  return;
    //}

    $wamp.call('users.findById', [id])
      .then(function(user) {
        if (user != null) {
          instance.normalizeUser(user);
          Cache.setItem(instance.userPrefix + user.id, user);
          callbackOk(user);

        } else {
          callbackError('Error');

        }
      }, function(err) {
        callbackError(err);
      });
  }


  this.updateUser = function(user, callbackOk, callbackError) {
    // elimino ese usuario de la cache
    //Cache.removeItem(instance.userPrefix + user.id);
    //instance.normalizeUser(user);

    $wamp.call('users.persistUser', [user])
      .then(function(res) {
        if (res != null) {
          callbackOk(res);
        } else {
          callbackError('Error');
        }
      }, function(err) {
        callbackError(err);
      });
  }


  this.listUsers = function(search, callbackOk, callbackError) {
    $wamp.call('users.findUsersIds')
      .then(function(ids) {
        if (ids != null) {

          // tengo los ids de las personas que existen en el server.
          var cachedUsers = [];
          var remainingIds = [];
          var ids = response.users;
          for (var i = 0; i < ids.length; i++) {
            var user = Cache.getItem(instance.userPrefix + ids[i].id);
            if (user == null) {
              remainingIds.push(ids[i].id);
            } else {
              cachedUsers.push(user);
            }
          }

          // si no hay mas usuarios que pedir. (tengo todos en la cache local)
          if (remainingIds.length <= 0) {
            callbackOk(cachedUsers);
            return;
          }

          $wamp.call('users.findUsersByIds', [remainingIds])
            .then(function(users) {
              if (users != null) {

                for (var i = 0; i < users.length; i++) {
                  var user = users[i];
                  instance.normalizeUser(user)
                  Cache.setItem(instance.userPrefix + user['id'], user);
                }
                callbackOk(cachedUsers.concat(response.users));

              } else {
                callbackError('Error');
              }
            }, function(err) {
              callbackError(err);
            });

        } else {
          callbackError('Error');
        }
      }, function(err) {
        callbackError(err);
      });
  };


  /*
    metodos nuevos usados por pablo. para reemplazar los viejos.
  */

  this.findAllMails = function(userId) {
    return $wamp.call('users.mails.findMails', [userId]);
  }

  this.persistMail = function(email) {
    return $wamp.call('users.mails.persistMail', [email]);
  }

  this.findByDni = function(dni) {
    return $wamp.call('users.findByDni', [dni]);
  }

  this.findById = function(id) {
    return $wamp.call('users.findById', [id]);
  }


};

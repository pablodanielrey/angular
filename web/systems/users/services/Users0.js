(function() {
    'use strict'
    angular
      .module('users')
      .service('Users',Users);

    Users.inject = ['$rootScope', 'Login', '$q'];

    function Users($rootScope, Login, $q) {
      /*
        NORMALIZACION DE USUARIO
      */
      this.fromIdsToUsers = fromIdsToUsers;         // transforma lista de [ids] a lista de [{id:id1}, {id:id2}, ...] para encardenar promesas
      this.findById = findById;
      this.findPhoto = findPhoto;
      this.findAll = findAll;
      this.findPhotos = findPhotos;

      function findAll() {
        return Login.getPrivateTransport().call('users.find_all');
      }

      function findById(ids) {
        if (ids.length <= 0) {
          return $q.when([]);
        }
        return Login.getPrivateTransport().call('users.find_by_id', [ids]);
      }

      function findPhoto(photoId) {
        return Login.getPrivateTransport().call('users.find_photo', [photoId]);
      };

      this.normalizeUser = function(user) {
        if (!('__json_module__' in user)) {
          user.__json_module__ =  'model.users.users';
        }

        if (!('__json_class__' in user)) {
          user.__json_class__ = 'User';
        }

        if (user.telephones && user.telephones.length > 0) {
            user.telephones = this.normalizeTelephones(user.telephones);
        }

        return user;
      }

      this.normalizeTelephones = function(telephones) {
        ret = []
        for (var i = 0; i < telephones.length; i++) {
          t = telephones[i];
          if (!('__json_module__' in t)) {
            t.__json_module__ =  'model.users.users';
          }

          if (!('__json_class__' in t)) {
            t.__json_class__ = 'Telephone';
          }
          ret.push(t);
        }
        return ret;
      }



      this.findByDni = function(dni) {
        return new Promise(function(cok, cerr) {
          Login.getPrivateTransport().call('users.findByDni', [dni])
          .then(function(data) {
            if (data == null) {
              cerr(Error('No existe ese usuario'));
              return;
            };
            var id = data[0];
            var version = data[1];
            Login.getPrivateTransport().call('users.findById', [[id]])
            .then(function(users) {
              cok(users);
            }, function(err) {
              cerr(err);
            });
          }, function(err) {
            cerr(err);
          });
        });
      }

      var instance = this;
      this.userPrefix = 'user_';

      $rootScope.$on('UserUpdatedEvent', function(event,id) {
        Cache.removeItem(instance.userPrefix + id);
      });

        this.deleteMail = function(id, callbackOk, callbackError) {
          Login.getPrivateTransport().call('users.mails.deleteMail', [id])
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
        Login.getPrivateTransport().call('users.mails.confirmEmail', [hash])
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
        Login.getPrivateTransport().call('users.mails.sendEmailConfirmation', [id])
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
        Login.getPrivateTransport().call('users.mails.persistMail', [userId, email])
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
        Login.getPrivateTransport().call('users.mails.findMails', [userId])
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



      this.findUser = function(id, callbackOk, callbackError) {

        // chequeo la cache primero
        //var user = Cache.getItem(instance.userPrefix + id);
        //if (user != null) {
        //  callbackOk(user);
        //  return;
        //}

        Login.getPrivateTransport().call('users.findById', [id])
          .then(function(user) {
            if (user != null) {
              user = this.normalizeUser(user);
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

        user = this.normalizeUser(user);

        Login.getPrivateTransport().call('users.persistUser', [user])
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
        Login.getPrivateTransport().call('users.findUsersIds')
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

              Login.getPrivateTransport().call('users.findUsersByIds', [remainingIds])
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

      /*
        Transforma una lisa de ids : [id1, id2, id3, .....]
        a una lista de objetos de tipo user con el id cargado : [{id:id1},{id:id2},{id:id3},.....]
        asi se pueden encadenar promesas que vayan cargando datos de los usuarios sin necesidad de tener que armar el código de creación de
        objetos usuarios.
        ej para buscar solo las fotos de ciertos ids que se tienen sin buscar los datos de los usuarios.
          fromIdsToUsers(['sdfdsf','23432','sdfdsfs']).then(findPhotos).then(findMails).......
      */
      function fromIdsToUsers(ids) {
        if (ids.length <= 0) {
          return $q.when([]);
        }
        var users = [];
        for (var i = 0; i < ids.length; i++) {
          users[i] = {id: ids[i]};
        }
        var d = $q.defer();
        d.resolve(users);
        return d.promise;
      }

      /*
        recibe una lista de usuarios con id y carga la photo dentro de la lista y la retorna.
        [{
          id: isUsuario
          photo: base64 de la foto.
        }]
        se puede encadenar con promesas que retornen la lista de usuarios. Ej findByIds(ids).then(findPhotos).then......
      */
      function findPhotos(users) {
        if (users.length <= 0) {
          return $q.when(users);
        }
        return Login.getPrivateTransport().call('users.find_photos', [users]);
      }

      this.findAllMails = function(userId) {
        return Login.getPrivateTransport().call('users.mails.findMails', [userId]);
      }

      this.persistMail = function(email) {
        return Login.getPrivateTransport().call('users.mails.persistMail', [email]);
      }

      this.removeMail = function(id) {
        return Login.getPrivateTransport().call('users.mails.deleteMail', [id]);
      }

      // esto lo modifique solo para obtener el usuario por dni, no se como se deberia manejar con la cache
    };

})();

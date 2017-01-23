(function() {
    'use strict'
    angular
      .module('users')
      .service('Users',Users);

    Users.inject = ['$rootScope', 'Login', '$q', 'Files'];

    function Users($rootScope, Login, $q, Files) {

      //Buscar usuarios a partir de un string
      //@param search Busqueda
      this.search = function (search){ return Login.getPrivateTransport().call('users.search', [search]); }

      //Administrar (define un usuario para administracion)
      //@param id de usuario o null (si esta definido el id buscara el usuario en la base)
      this.admin = function(id){ return Login.getPrivateTransport().call('users.admin', [id]); }

      //Persistir usuario
      //@param user User a persistir
      this.persist = function(user){ return Login.getPrivateTransport().call('users.persist', [user]); }


      this.fromIdsToUsers = fromIdsToUsers;         // transforma lista de [ids] a lista de [{id:id1}, {id:id2}, ...] para encardenar promesas
      this.fromUserToList = fromUserToList;
      this.findByIds = findByIds;
      this.findByDni = findByDni;
      this.findAll = findAll;
      this.findPhotos = findPhotos;
      this.findPhoto = findPhoto;
      this.photoToDataUri = photoToDataUri;






      //////////////////// INDICES SECUNDARIOS /////////////////////////////
      // métodos que retornan listas de ids de usuarios
      /////////////////////////

      /*
        retorna los ids de las personas que tienen los dnis indicados
      */
      function findByDni(dnis) {
        if (dnis.length <= 0) {
          return $q.when([]);
        }
        return Login.getPrivateTransport().call('users.find_by_dni', [dnis]);
      }

      function findAll() {
        return Login.getPrivateTransport().call('users.find_all');
      }

      ///////////////////////////////////////////////////////////////////



      function findByIds(ids) {
        if (ids.length <= 0) {
          return $q.when([]);
        }
        return Login.getPrivateTransport().call('users.find_by_ids', [ids]);
      }

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
          _toUserObject(users[i]);
        }
        var d = $q.defer();
        d.resolve(users);
        return d.promise;
      }

      /*
        Usada en la conversión de ids --> usuarios
      */
      function _toUserObject(user) {
        if (!('__json_module__' in user)) {
          user.__json_module__ =  'model.users.users';
        }

        if (!('__json_class__' in user)) {
          user.__json_class__ = 'User';
        }
      }

      /*
        Transforma un usuario en una lista. asi puede ser encadenado con los otros métodos.
        ej:
          fromUserToList(user).then(findPhotos).then....
      */
      function fromUserToList(user) {
        if (user == null) {
          return $q.when([]);
        }
        var d = $q.defer();
        d.resolve([user]);
        return d.promise;
      }


      /////////////////////// METODOS PARA OBTENER DATOS DE LOS USUARIOS /////////////////////////////////////
      ///
      /// Manejan listas de usuarios, principalmente cargado el id y cargan los datos obtenidos dentro de las listas.
      ///
      ///  Ej : [{id: id1}, {id:id2}, {id:id3}, .... ] ---> [{id:id1, photo:"...."}, {id:id2, photo:"...."}, {id:id3, photo:"...."}]
      ///
      ///////////////////////////////////////////////////////////////////////////////////////

      function findPhotos(users) {
        if (users.length <= 0) {
          return $q.when(users);
        }
        return Login.getPrivateTransport().call('users.find_photos', [users]);
      }

      /*
        Transforma la foto a un data uri para poder mostrarla direcamente dentro de las páginas.
      */
      function photoToDataUri(users) {
        for (var i = 0; i < users.length; i++) {
          users[i].photoSrc = (users[i].photo == null) ? '' : Files.toDataUri(users[i].photo);
        }
        return $q.when(users);
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

      function findPhoto(photoId) {
        return Login.getPrivateTransport().call('users.find_photo', [photoId]);
      }

  }
})();

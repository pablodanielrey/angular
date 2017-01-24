(function() {
    'use strict';

    angular
        .module('users')
        .service('Utils', Utils);

    Utils.$inject = ['Users', '$q', '$window', '$timeout'];

    /* @ngInject */
    function Utils(Users, $q, $window, $timeout) {

      //Administrar (define un usuario para administracion)
      //@param id de usuario o null (si esta definido el id buscara el usuario en la base)
      this.admin = function(id){
        return Users.admin(id).then(
          function(user){
            var types = (!user.type) ? [] : user.type.split(" ");
            user.types = [];
            for(var i = 0; i < types.length; i++) user.types.push({description:types[i]});
            return user;
          }
        )
      }

      //Persistir usuario
      //@param user User a persistir
      this.persist = function(user){
        var types = [];
        for(var i = 0; i < user.types.length; i++) types.push(user.types[i].description);
        user.type = types.join(" ")

        return Users.persist(user);
      }



        this.getOfficeTypes = getOfficeTypes;
        this.findAll = findAll;
        this.findByIds = findByIds;
        this.remove = remove;

        function getOfficeTypes() {
          /*
          var officesTypes = $window.sessionStorage.getItem("officesTypes");
          if (officesTypes != null) {
            var d = $q.defer();
            d.resolve(JSON.parse(officesTypes));
            return d.promise;
          }
          */

          return Offices.getOfficeTypes().then(
                function(types) {
                  $window.sessionStorage.setItem("officesTypes", JSON.stringify(types[0]));
                  return types[0];
                });
        }


        function findAll(types) {
          var d = $q.defer();

          Offices.findAll(types).then(
            function(ids) {
              findByIds(ids).then(
                function(offices) {
                  var offices_ = []
                  for(var i = 0; i < offices.length; i++){
                    var o = offices[i]
                    o.type = {name:offices[i].type, value:offices[i].type}
                    offices_.push(o)
                  }
                  d.resolve(offices_);
                }
              )
            }
          );

          return d.promise;
        }

        function findByIds(ids) {
          var promises = [];
          for(var i = 0; i < ids.length; i++) {
            promises.push(findById(ids[i]));
          }
          return $q.all(promises);
        }

        function findById(id) {
          /*
          var off = $window.sessionStorage.getItem(id);
          if (off != null) {
            var d = $q.defer();
            d.resolve(JSON.parse(off));
            return d.promise;
          }
          */

          return Offices.findById([id]).then(
                function(offices) {
                  if (offices.length > 0) {
                    var office = offices[0];
                    office.type = (office.type == null) ? {value: null} : office.type;
                    $window.sessionStorage.setItem(offices[0].id, JSON.stringify(office))
                  }
                  return offices[0];
                }
              );

        }

        function remove(office) {
          $window.sessionStorage.removeItem(office.id);
          return Offices.remove(office);
        }
/*
        function persist(office) {
          var off = convertOffice(office);
          return Offices.persistWithUsers(off, office.users);
        }*/

        function convertOffice(office) {
          var off = {};
          off.name = office.name;
          off.type = office.type.value;
          off.parent = (office.parentObj == null) ? null : office.parentObj.id;
          off.number = office.number;
          off.telephone = office.telephone;
          off.email = office.email;
          off.public = office.public;
          off.id = office.id;
          off.__json_class__ = 'Office';
          off.__json_module__ = "model.offices.office"

          console.log(JSON.stringify(off));

          return off;
        }



    }
})();

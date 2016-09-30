(function() {
    'use strict';

    angular
        .module('offices')
        .service('Utils', Utils);

    Utils.$inject = ['Offices', '$q', '$window', '$timeout'];

    /* @ngInject */
    function Utils(Offices, $q, $window, $timeout) {

        this.getOfficeTypes = getOfficeTypes;
        this.findAll = findAll;
        this.findByIds = findByIds;
        this.persist = persist;
        this.remove = remove;

        function getOfficeTypes() {
          var officesTypes = $window.sessionStorage.getItem("officesTypes");
          if (officesTypes != null) {
            var d = $q.defer();
            d.resolve(JSON.parse(officesTypes));
            return d.promise;
          }

          return Offices.getOfficeTypes().then(
                function(types) {
                  $window.sessionStorage.setItem("officesTypes", JSON.stringify(types));
                  return types;
                });
        }


        function findAll(types) {
          var d = $q.defer();

          Offices.findAll(types).then(
            function(ids) {
              findByIds(ids).then(
                function(offices) {
                  d.resolve(offices);
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
          var off = $window.sessionStorage.getItem(id);
          if (off != null) {
            var d = $q.defer();
            d.resolve(JSON.parse(off));
            return d.promise;
          }

          return Offices.findById([id]).then(
                function(offices) {
                  if (offices.length > 0) {
                    $window.sessionStorage.setItem(offices[0].id, JSON.stringify(offices[0]))
                  }
                  return offices[0];
                }
              );

        }

        function remove(office) {
          $window.sessionStorage.removeItem(office.id);
          return Offices.remove(office);
        }

        function persist(office) {
          var off = convertOffice(office);
          return Offices.persist(off);
        }

        function convertOffice(office) {
          var off = {};
          off.name = office.name;
          off.type = office.type.value;
          off.parent = (office.parentObj == null) ? null : office.parentObj.id;
          off.number = office.number;
          off.telephone = office.telephone;
          off.id = office.id;
          off.__json_class__ = 'Office';
          off.__json_module__ = "model.offices.office"

          console.log(JSON.stringify(off));

          return off;
        }



    }
})();

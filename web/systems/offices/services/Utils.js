(function() {
    'use strict';

    angular
        .module('offices')
        .service('Utils', Utils);

    Utils.$inject = ['Offices', '$q', '$window'];

    /* @ngInject */
    function Utils(Offices, $q, $window) {

        this.getOfficeTypes = getOfficeTypes;
        this.findAll = findAll;
        this.findByIds = findByIds;

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



    }
})();

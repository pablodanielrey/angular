(function() {
    'use strict';

    angular
        .module('users')
        .service('Utils', Utils);

    Utils.$inject = ['Users', '$q'];

    /* @ngInject */
    function Utils(Users, $q) {


    }
})();

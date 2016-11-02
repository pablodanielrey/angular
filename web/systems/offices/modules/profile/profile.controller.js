(function() {
    'use strict'
    angular
      .module('offices')
      .controller('ProfileCtrl');

    ReportsCtrl.$inject = ['$scope', 'Assistance', 'Users', '$timeout', 'Login', '$window', 'Offices', '$filter'];

    function ProfileCtrl($scope, Assistance, Users, $timeout, Login, $window, Offices, $filter) {
        var vm = this;
    }


})();

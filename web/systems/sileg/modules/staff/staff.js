(function() {
    'use strict';

    angular
        .module('sileg')
        .controller('StaffCtrl', StaffCtrl);

    StaffCtrl.$inject = ['$scope', '$location', '$timeout', '$window', '$q', 'SilegDD'];

    function StaffCtrl($scope, $location, $timeout, $window, $q, SilegDD) {
        var vm = this;

        vm.model = {}; //variables del controlador
        vm.view = {cathedras:[], users:[], positions:[]};

        vm.selectUser = selectUser;
        vm.selectCathedra = selectCathedra;

        function selectUser(user){
          vm.view.style2 = 'verInfoDocente';
          vm.view.user = user;
          /*
          SilegDD.getPositionsByUser(user).then(
            function(positions){ vm.view.positions = positions; },
            function(error){ console.log(error); }
          )*/
        };

        function selectCathedra(cathedra){
          vm.view.style2 = 'verInfoCatedra';
          vm.view.cathedra = cathedra;

          /*
          SilegDD.getPositionsByCathedra(user).then(
            function(positions){ vm.view.positions = positions; },
            function(error){ console.log(error); }
          )*/
        };


        activate();

        function activate(){
          SilegDD.getUsers().then(
              function(users){ vm.view.users = users; },
              function(error){ console.log(error); }
          );

          SilegDD.getCathedras().then(
              function(cathedras){ vm.view.cathedras = cathedras; },
              function(error){ console.log(error); }
          );
        }
    }
})();

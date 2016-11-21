(function() {
    'use strict';

    angular
        .module('sileg')
        .controller('StaffCtrl', StaffCtrl);

    StaffCtrl.$inject = ['$scope', '$location', '$timeout', '$window', '$q', 'SilegDD', 'Login'];

    function StaffCtrl($scope, $location, $timeout, $window, $q, SilegDD, Login) {
        var vm = this;

        vm.model = {}; //variables del controlador
        vm.view = {activate: false, places:[], users:[], positions:[]};

        vm.selectUser = selectUser;
        vm.selectPlace = selectPlace;

        function selectUser(user){
          vm.view.style2 = 'verInfoDocente';
          vm.view.user = user;

          SilegDD.findPositionsActiveByUser(user.id).then(
            function(positions){ vm.view.positions = positions;  },
            function(error){ console.log(error); }
          );
        };

        function selectPlace(place){
          vm.view.style2 = 'verInfoCatedra';
          vm.view.place = place;

          SilegDD.findPositionsActiveByPlace(place.id).then(
            function(positions){ vm.view.positions = positions;  },
            function(error){ console.log(error); }
          );
        };

        $scope.$on('wamp_public.open', function(event, args) {
          activate();
        });


        function activate(){
          if (vm.view.activate || Login.getPublicTransport() == null) return;
            
          vm.view.activate = true;

          SilegDD.getUsers().then(
              function(users){ vm.view.users = users; },
              function(error){ console.log(error); }
          );

          SilegDD.getPlaces().then(
              function(places){ vm.view.places = places; },
              function(error){ console.log(error); }
          );
        }
    }
})();

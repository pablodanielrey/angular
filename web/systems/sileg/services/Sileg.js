(function() {
		'use strict'
		angular
			.module('sileg')
			.service('Sileg', Sileg);

		Sileg.inject = ['$window', '$q', 'Login'];

		function Sileg($window, $q, Login) {

		  this.getUsers = getUsers;
			this.getPlaces = getPlaces;
			this.findPositionsActiveByUser = findPositionsActiveByUser;
			this.findPositionsActiveByPlace = findPositionsActiveByPlace;



		  function getUsers() {  return Login.getPublicTransport().call('sileg.get_users');  };
      function getPlaces() {  return Login.getPublicTransport().call('sileg.get_cathedras');  };
			function findPositionsActiveByUser(userId) {  return Login.getPublicTransport().call('sileg.find_positions_active_by_user', [userId]);  };
			function findPositionsActiveByPlace(placeId) {  return Login.getPublicTransport().call('sileg.find_positions_active_by_place', [placeId]);  };

		}



})();

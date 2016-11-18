(function() {
		'use strict'
		angular
			.module('sileg')
			.service('Sileg', Sileg);

		Sileg.inject = ['$window', '$q', 'Login'];

		function Sileg($window, $q, Login) {

		  this.getUsers = getUsers;
			this.getCathedras = getCathedras;
			this.findPositionsActiveByUser = findPositionsActiveByUser;



		  function getUsers() {  return Login.getPublicTransport().call('sileg.get_users');  };
      function getCathedras() {  return Login.getPublicTransport().call('sileg.get_cathedras');  };
			function findPositionsActiveByUser(userId) {  return Login.getPublicTransport().call('sileg.find_positions_active_by_user', [userId]);  };



		}



})();

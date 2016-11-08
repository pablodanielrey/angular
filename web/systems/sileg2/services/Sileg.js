(function() {
		'use strict'
		angular
			.module('sileg')
			.service('Sileg', Sileg);

		Sileg.inject = ['$window', '$q'];

		function Sileg($window, $q) {

		  this.searchUsers = searchUsers;

		  function searchUsers(regex) {
		    return Login.getPrivateTransport().call('issues.search_users', [regex]);
  		  }
		}

})();

(function() {
		'use strict'
		angular
			.module('offices')
			.service('Offices', Offices);

		Offices.inject = ['Login'];

		function Offices(Login) {

			this.subscribe = subscribe;
		  this.findById = findById;
			this.getOfficesByUser = getOfficesByUser;
			this.searchUsers = searchUsers;

			function subscribe(event, func) {
				Login.getPrivateTransport().subscribe(event, func);
			}

			function findById(ids) {
				return Login.getPrivateTransport().call('offices.find_by_id',[ids]);
			}

			function getOfficesByUser(userId, tree) {
				return Login.getPrivateTransport().call('offices.find_offices_by_user',[user_id, tree]);
			}

			function searchUsers(regex) {
				return Login.getPrivateTransport().call('offices.search_users', [regex]);
			}
		}

})();

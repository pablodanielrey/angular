(function() {
		'use strict'
		angular
			.module('offices')
			.service('Offices',Offices);

		Offices.inject = ['Login'];

		function Offices(Login) {

			this.$wamp = Login.getTransport().private;

			this.getOfficesByUser = function (userId, tree) {
				return this.$wamp.call('offices.find_offices_by_user', [userId, tree]);
			}

			this.findById = function (ids) {
				return this.$wamp.call('offices.find_by_id',[ids]);
			}

		};

})();

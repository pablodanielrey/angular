(function() {
		'use strict'
		angular
			.module('assistance')
			.service('Assistance', Assistance);

		Assistance.inject = ['Login'];

		function Assistance(Login) {
      this.getLogs = getLogs;

      function getLogs() {
        return Login.getPrivateTransport().call('assistance.get_logs');
      }

    }
})();

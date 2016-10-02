(function() {
		'use strict'
		angular
			.module('assistance')
			.service('Assistance', Assistance);

		Assistance.inject = ['Login'];

		function Assistance(Login) {
      this.getLogs = getLogs;

      function getLogs(initDate, endDate) {
        var di = initDate.toISOString();
				var de = endDate.toISOString();
        return Login.getPrivateTransport().call('assistance.get_logs', [di,de]);
      }

    }
})();

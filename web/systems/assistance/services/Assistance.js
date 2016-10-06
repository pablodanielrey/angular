(function() {
		'use strict'
		angular
			.module('assistance')
			.service('Assistance', Assistance);

		Assistance.inject = ['Login'];

		function Assistance(Login) {

      this.getLogs = getLogs;
			this.getStatistics = getStatistics;
			this._formatDateDay = _formatDateDay;
			this._formatDateHour = _formatDateHour;

			function _formatDateDay(d) {
	      return d.getDate() + '/' + d.getMonth() + '/' + d.getFullYear()
	    }

	    function _formatDateHour(d) {
	      return d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds();
	    }


      function getLogs(initDate, endDate) {
        var di = initDate.toISOString();
				var de = endDate.toISOString();
        return Login.getPrivateTransport().call('assistance.get_logs', [di,de]);
      }

			function getStatistics(initDate, endDate, userIds) {
				var di = initDate.toISOString();
				var de = endDate.toISOString();
				return Login.getPrivateTransport().call('assistance.get_statistics', [di,de,userIds])
			}

    }
})();

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

			/*
				Setea los usuarios a los logs
				Ej: [{userId:id1},{userId:id2}]
				retorna: [{userId:id1, user: user1}, {userId: id2, user: user2}]
			*/
			function findUsersById(logs) {
				var uids = [];
	      for (var i = 0; i < logs.length; i++) {
	        uids.push(logs[i].userId);
	      }
				return Users.findById(uids).then(
					function(users) {
						for (var i = 0; i < logs.length; i++) {
							for(var j = 0; j < users.length; j++) {
								if (logs[i].userId == users[j].id) {
									logs[i].user = users[i];
									break;
								}
							}
						}
						return logs;
					}
				);
			}

			/*
			Setea el atributo photo al user del log
			Ej: [{user: user1, userId: id1}, {user: user2, userId: id2}]
			*/

    }
})();

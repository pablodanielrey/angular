(function() {
		'use strict'
		angular
			.module('assistance')
			.service('Assistance', Assistance);

		Assistance.inject = ['Login', 'Users'];

		function Assistance(Login, Users) {

      this.getLogs = getLogs;
			this.getStatistics = getStatistics;
			this._formatDateDay = _formatDateDay;
			this._formatDateHour = _formatDateHour;

			this.findUsersByLogs = findUsersByLogs;
			this.findUserPhotos = findUserPhotos;
			this.photoToDataUri = photoToDataUri;

			this.findUsersByStatics = findUsersByStatics;

			function _formatDateDay(d) {
	      return d.getDate() + '/' + d.getMonth() + '/' + d.getFullYear()
	    }

	    function _formatDateHour(d) {
	      return d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds();
	    }


      function getLogs(initDate, endDate, initHour, endHour) {
        var di = initDate.toISOString();
				var de = endDate.toISOString();
				var hi = initHour.toISOString();
				var he = endHour.toISOString();
        return Login.getPrivateTransport().call('assistance.get_logs', [di,de, hi, he]);
      }


			/*
				Setea los usuarios a los logs
				Ej: [{userId:id1},{userId:id2}]
				retorna: [{userId:id1, user: user1}, {userId: id2, user: user2}]
			*/
			function findUsersByLogs(logs) {
				var uids = [];
	      for (var i = 0; i < logs.length; i++) {
					uids.push(logs[i].userId);
				}
				return Users.findById(uids).then(
					function(users) {
						for (var i = 0; i < logs.length; i++) {
							for(var j = 0; j < users.length; j++) {
								if (logs[i].userId == users[j].id) {
									logs[i].user = users[j];
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
			function findUserPhotos(logs) {
				var users = [];
				for (var i = 0; i < logs.length; i++) {
					if (logs[i].user) {
						users.push(logs[i].user);
					} else {
						console.log(logs[i])
					}
				}

				return Users.findPhotos(users).then(
						function(users) {
							for (var i = 0; i < logs.length; i++) {
								for(var j = 0; j < users.length; j++) {
									if (logs[i].userId == users[j].id) {
										logs[i].user = users[j];
										break;
									}
								}
							}
							return logs;
						}
					);
				}

			/*
	        Transforma la foto a un data uri para poder mostrarla direcamente dentro de las páginas.
	    */
			function photoToDataUri(logs) {
				var users = [];
				for (var i = 0; i < logs.length; i++) {
					if (logs[i].hasOwnProperty('user')) {
						users.push(logs[i].user);
					}
				}

				return Users.photoToDataUri(users).then(
						function(users) {
							for (var i = 0; i < logs.length; i++) {
								for(var j = 0; j < users.length; j++) {
									if (logs[i].userId == users[j].id) {
										logs[i].user = users[j];
										break;
									}
								}
							}
							return logs;
						}
					);
				}

				/* ***********************************************************************************
																					ESTADISTICAS
				 * *********************************************************************************** */

				/*
				stats= [{date: "2016-10-17T00:00:00+00:00",
								logStart: "2016-10-17T09:14:42+00:00",
							  logEnd: "2016-10-17T15:14:42+00:00",
								scheduleStart: "2016-10-17T06:00:00+00:00",
								scheduleEnd: "2016-10-17T13:00:00+00:00",
								userId: userId1,
								position: 'E5',
								workedSeconds: 23134,
								justification: {

								}
							]

					*/

				function getStatistics(initDate, endDate, userIds, officeIds, initTime, endTime) {
					var di = initDate.toISOString();
					var de = endDate.toISOString();
					var ti = initTime.toISOString();
					var te = endTime.toISOString();
					return Login.getPrivateTransport().call('assistance.get_statistics', [di,de,userIds, officeIds, ti, te])
				}

				/*
					Setea los usuarios a las estadisticas
					Ej: [{userId:id1},{userId:id2}]
					retorna: [{userId:id1, user: user1}, {userId: id2, user: user2}]
				*/
				function findUsersByStatics(stats) {
					var uids = [];
		      for (var i = 0; i < stats.length; i++) {
						uids.push(stats[i].userId);
					}
					return Users.findById(uids).then(
						function(users) {
							for (var i = 0; i < stats.length; i++) {
								for(var j = 0; j < users.length; j++) {
									if (stats[i].userId == users[j].id) {
										stats[i].user = users[j];
										break;
									}
								}
							}
							return stats;
						}
					);
				}

    }
})();

(function() {
		'use strict'
		angular
			.module('assistance')
			.service('Assistance', Assistance);

		Assistance.inject = ['Login', 'Users', '$q'];

		function Assistance(Login, Users, $q) {

      this.getLogs = getLogs;
			this.exportLogs = exportLogs;

			this.getStatistics = getStatistics;
			this.exportStatistics = exportStatistics;

			this.findUsersByLogs = findUsersByLogs;
			this.findUserPhotos = findUserPhotos;
			this.photoToDataUri = photoToDataUri;

			this.findUsersByStatics = findUsersByStatics;
			this.setWorkedNote = setWorkedNote;

			this.searchUsers = searchUsers;
			this.findUserByIds = findUserByIds;
			this.loadProfile = loadProfile;

			this.saveSpecialSchedules = saveSpecialSchedules;
			this.loadWatcherSchedules = loadWatcherSchedules;
			this.loadSchedules = loadSchedules;
			this.saveWatcherSchedules = saveWatcherSchedules;
			this.saveSchedules = saveSchedules;


      function getLogs(initDate, endDate, initHour, endHour) {
        var di = initDate.toISOString();
				var de = endDate.toISOString();
				var hi = initHour.toISOString();
				var he = endHour.toISOString();
        return Login.getPrivateTransport().call('assistance.get_logs', [di, de, hi, he]);
      }

			function exportLogs(initDate, endDate, initHour, endHour) {
        var di = initDate.toISOString();
				var de = endDate.toISOString();
				var hi = initHour.toISOString();
				var he = endHour.toISOString();
        return Login.getPrivateTransport().call('assistance.export_logs', [di, de, hi, he]);
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

				 function exportStatistics(initDate, endDate, userIds, officeIds, initTime, endTime) {
						var di = initDate.toISOString();
						var de = endDate.toISOString();
						var ti = initTime.toISOString();
						var te = endTime.toISOString();
						return Login.getPrivateTransport().call('assistance.export_statistics', [di,de, userIds, officeIds, ti, te])
				 }

				 function setWorkedNote(userId, date, text) {
					 return Login.getPrivateTransport().call('assistance.set_worked_note', [userId, date, text])
				 }

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
					var di = (initDate == null) ? null : initDate.toISOString();
					var de = (endDate == null) ? null : endDate.toISOString();
					var ti = (initTime == null) ? null : initTime.toISOString();
					var te = (endTime == null) ? null : endTime.toISOString();
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

				/* ***********************************************************************************
																					Usuarios de asistencia
				 * *********************************************************************************** */

				 function findUserByIds(users) {
					 var d = $q.defer();
					  var ids = [];
					 	for (var i = 0; i < users.length; i++) {
							ids.push(users[i].id);
						}
						Users.findById(ids).then(function(users) {
							console.log(users);
							d.resolve(users);
						}, function(error) {
							d.reject(error);
						});

						return d.promise;
				 }

				/*
					searchUsers return : [(userId, version)]
				*/
				function searchUsers(regex) {
					var d = $q.defer();
					Login.getPrivateTransport().call('assistance.search_users', [regex]).then(function(ids) {
						var users = [];
						for (var i = 0; i < ids.length; i++) {
							var data = ids[i];
							users.push({id:data[0], version: data[1]});
						}
						d.resolve(users);
					}, function(error) {
						d.reject(error);
					});
					return d.promise;
				}

				// return: 'admin' o 'user'
				function loadProfile() {
					var defer = $q.defer();
					defer.resolve('admin');
					return defer.promise;
				}

				/* ***********************************************************************************
																					SCHEDULES
				 * *********************************************************************************** */

				 function saveSpecialSchedules(schedules) {
					 var defer = $q.defer();
 					defer.resolve(true);
 					return defer.promise;
				 }

				 function saveSchedules(schedules) {
					 var defer = $q.defer();
 					defer.resolve(true);
 					return defer.promise;
				 }

				 function saveWatcherSchedules(schedules) {
					 var defer = $q.defer();
 					defer.resolve(true);
 					return defer.promise;
				 }

				 function loadWatcherSchedules(date) {
					 var defer = $q.defer();
					 var schedules = [];
					 var start = new Date(); start.setHours(21); start.setMinutes(0); start.setSeconds(0); start.setMilliseconds(0);
           schedules.push({day:"2", start: start, hours: 25});
           start = new Date(); start.setHours(15); start.setMinutes(0); start.setSeconds(0); start.setMilliseconds(0);
           schedules.push({day:"4", start: start, hours: 30});
					 defer.resolve(schedules);
					 return defer.promise;
				 }

				 function loadSchedules(date) {
					 var defer = $q.defer();
					 var schedules = [];
					 var dayMillis = 24 * 60 * 60 * 1000;
					 for (var i = 0; i < 7; i++) {
						 var dateAux = new Date(date.getTime() + i * dayMillis);
						 if (dateAux.getDay() == 6 || dateAux.getDay() == 0) {
							 schedules.push({date: dateAux, start: null, end: null, style: 'horarioNormal'});
							 continue;
						 }

						 if (dateAux.getDay() == 3) {
							 var start = new Date(dateAux.getTime());
							 var end = new Date(dateAux.getTime());
							 start.setHours(7); start.setMinutes(0); start.setSeconds(0); start.setMilliseconds(0);
							 end.setHours(10); end.setMinutes(30); end.setSeconds(0); end.setMilliseconds(0);
							 schedules.push({date: dateAux, start: start, end: end, style: 'horarioNormal'});
							 var start = new Date(dateAux.getTime());
							 var end = new Date(dateAux.getTime());
							 start.setHours(15); start.setMinutes(30); start.setSeconds(0); start.setMilliseconds(0);
							 end.setHours(19); end.setMinutes(0); end.setSeconds(0); end.setMilliseconds(0);
							 schedules.push({date: dateAux, start: start, end: end, style: 'horarioCortado'});
						 } else {
							 var start = new Date(dateAux.getTime());
							 var end = new Date(dateAux.getTime());
							 start.setHours(8); start.setMinutes(0); start.setSeconds(0); start.setMilliseconds(0);
							 end.setHours(15); end.setMinutes(0); end.setSeconds(0); end.setMilliseconds(0);
							 schedules.push({date: dateAux, start: start, end: end, style: 'horarioNormal'});
						 }
					 }

					 defer.resolve(schedules);
					 return defer.promise;
				 }

    }
})();

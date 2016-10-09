(function() {
		'use strict'
		angular
			.module('offices')
			.service('Offices', Offices);

		Offices.inject = ['Login','$q'];

		function Offices(Login, $q) {

			this.subscribe = subscribe;
		  this.findById = findById;
			this.searchUsers = searchUsers;
			this.findUsersByIds = findUsersByIds;
			this.getOfficeTypes = getOfficeTypes;
			this.findByUser = findByUser;
			this.findByUserAndTypes = findByUserAndTypes;
			this.getOfficesByUser = getOfficesByUser;
			this.findAll = findAll;
			this.persist = persist;
			this.persistWithUsers = persistWithUsers;
			this.remove = remove;
			this.runAndConcat = runAndConcat;

			function subscribe(event, func) {
				Login.getPrivateTransport().subscribe(event, func);
			}

			function findById(ids) {
				if (ids == null || ids.length <= 0)  {
					return $q.when([]);
				}
				return Login.getPrivateTransport().call('offices.find_by_id',[ids]);
			}

			function findByUser(userId, tree) {
				if (userId == null) {
					return [];
				}
				return Login.getPrivateTransport().call('offices.find_offices_by_user',[userId, null, tree]);
			}

			function findByUserAndTypes(userId, types, tree) {
				if (userId == null) {
					return [];
				}
				return Login.getPrivateTransport().call('offices.find_offices_by_user',[userId, types, tree]);
			}

			/*
				ejecuta las promesas y retorna la lista resultante de la concatenacion de los resultados.
			*/
			function runAndConcat(promises) {
				var d = $q.defer()
				$q.all(promises).then(function(lists) {
					var listr = [];
					for (var i = 0; i < lists.length; i++) {
						listr = listr.concat(lists[i]);
					}
					d.resolve(listr);
				});
				return d.promise;
			}

			/*
				Solo para no romper codigo anterior. ahora es findByUser
			*/
			function getOfficesByUser(userId, tree) {
				return findByUser(userId, tree);
			}

			function searchUsers(regex) {
				return Login.getPrivateTransport().call('offices.find_users_by_regex', [regex]);
			}

			function findUsersByIds(uids) {
				return Login.getPrivateTransport().call('offices.find_users_by_ids', [uids])
			}

			function getOfficeTypes() {
				return Login.getPrivateTransport().call('offices.get_office_types', []);
			}

			function findAll(types) {
				return Login.getPrivateTransport().call('offices.find_all', [types]);
			}

			function persist(office) {
				return Login.getPrivateTransport().call('offices.persist', [office]);
			}

			function persistWithUsers(office, userIds) {
				return Login.getPrivateTransport().call('offices.persist_with_users', [office, userIds]);
			}

			function remove(office) {
				return Login.getPrivateTransport().call('offices.remove', [office]);
			}

		}

})();

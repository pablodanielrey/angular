(function() {
		'use strict'
		angular
			.module('issues')
			.service('Issues', Issues);

		Issues.inject = ['Login', '$window', '$q'];

		function Issues(Login, $window, $q) {

		  this.getMyIssues = getMyIssues;
		  this.getOfficesIssues = getOfficesIssues;
		  this.getAssignedIssues = getAssignedIssues;
		  this.findById = findById;
			this.findByIds = findByIds;
			this.findAll = findAll;
		  this.create = create;
		  this.createComment = createComment;
		  this.changeStatus = changeStatus;
			this.changePriority = changePriority;
			this.getOffices = getOffices;
			this.getAreas = getAreas;
			this.getOfficeSubjects = getOfficeSubjects;
			this.subscribe = subscribe;
			this.searchUsers = searchUsers;
			this.updateIssue = updateIssue;

			function subscribe(event, func) {
				Login.getPrivateTransport().subscribe(event, func);
			}

		  function searchUsers(regex) {
				return Login.getPrivateTransport().call('issues.search_users', [regex]);
			}


		  function getOfficesIssues() {
				return Login.getPrivateTransport().call('issues.get_offices_issues');
			}

			/*
				busca todos los ids de los pedidos de acuerdo a los filtros pasados como parámetro.
				statuses = lista de ids de estados
				froms = lista de ids de oficinas de origen de los pedidos
				tos = lista de ids de oficinas de destino de los pedidos
			*/
			function findAll(statuses, froms, tos) {
				return Login.getPrivateTransport().call('issues.find_all', [statuses, froms, tos]);
			}

		  function getAssignedIssues(statuses, froms, tos) {
				return Login.getPrivateTransport().call('issues.get_assigned_issues', [statuses, froms, tos]).then(_findFromCacheOrLoad).then(_cacheIssues);
			}

			function getMyIssues(statuses, froms, tos) {
				return Login.getPrivateTransport().call('issues.get_my_issues', [statuses, froms, tos]).then(_findFromCacheOrLoad).then(_cacheIssues);
			}

			function updateIssue(id, status, priority) {
				var item = JSON.parse($window.sessionStorage.getItem(id));
				if (item != null) {
					item.statusId = status;
					item.priority = priority;
					$window.sessionStorage.setItem(id, JSON.stringify(item));
				}

			}

		  function findById(id) {
				if (id == null) {
					return $q.when(null);
				}
				return Login.getPrivateTransport().call('issues.find_by_id', [id]);
			}

			function findByIds(ids) {
				if (ids.length <= 0) {
					return $q.when([]);
				}
				return Login.getPrivateTransport().call('issues.find_by_ids', [ids]);
			}



		  function create(subject, description, parentId, officeId, fromOfficeId, authorId, files) {
				return Login.getPrivateTransport().call('issues.create', [subject, description, parentId, officeId, fromOfficeId, authorId, files]).then(_asyncInvalidateCache)
			}

		  function createComment(subject, description, parentId, officeId, files) {
				return Login.getPrivateTransport().call('issues.create_comment', [subject, description, parentId, officeId, files]).then(_asyncInvalidateCache);
			}

		  function changeStatus(issue, status) {
				return Login.getPrivateTransport().call('issues.change_status', [issue, status]).then(_asyncInvalidateSingleIssueCache);
			}

		  function changePriority(issue, priority) {
				return Login.getPrivateTransport().call('issues.change_priority', [issue, priority]).then(_asyncInvalidateSingleIssueCache);
			}

			function getOffices() {
				return Login.getPrivateTransport().call('issues.get_offices',[]);
			}

			function getOfficeSubjects(officeId) {
				return Login.getPrivateTransport().call('issues.get_office_subjects',[officeId]);
			}

			function getAreas(officeId) {
				return Login.getPrivateTransport().call('issues.get_areas',[officeId]);
			}


			//////////////////////////// CAPA CACHE DEL SISTEMA EN EL CLIENTE ///////////////////////
			/// la cache se compone de un indice que cachea el findAll y un cache de cada entrada del indice.
			///
			/// assignedIssues --> cachea la lista de ids de issues asignados a la persona logueada que existen en el sistema
			///
			///  issue.id ---> cache de cada issue en particular dentro del cliente
			///
			///////

			/*
				Obtiene el issue desde la cache o lo carga usando findByIds
				param: [ id1, id2, id3, .... ]
				return: [ Issue, Issue, Issue, ..... ]
			*/
			function _findFromCacheOrLoad(ids) {
				var remainingIds = [];

				// cargo desde la cache los issues existentes
				var issues = [];
				for (var i = 0; i < ids.length; i++) {
					var iss = $window.sessionStorage.getItem(ids[i]);
					if (iss != null) {
						issues.push(JSON.parse(iss));
					} else {
						remainingIds.push(ids[i]);
					}
				}

				// si estaban todos los ids pedidos en la cache
				if (remainingIds.length <= 0) {
					return $q.when(issues);
				}

				// si no, cargo lso que faltan desde el servidor usando findByIds, los cacheo y retorno tda la lista.
				var d = $q.defer();
				findByIds(remainingIds).then(_cacheIssues).then(function(iss) {
					var totalIssues = issues.concat(iss);
					return d.resolve(totalIssues);
				});
				return d.promise;
			}



			/*
				Cachea la lista de ids de issues que estan asignados a la persona
			*/
			function _asyncCacheAssignedIssuesIndex(issueIds) {
				$window.sessionStorage.setItem('assignedIssues', JSON.stringify(issueIds));
				$q.when(issueIds)
			}

			/*
				Cachea la lista de ids de issues que realizó la persona
			*/
			function _asyncCacheMyIssuesIndex(issueIds) {
				$window.sessionStorage.setItem('myIssues', JSON.stringify(issueIds));
				$q.when(issueIds)
			}


			/*
				Cachea los issues dentro de la cache, solo si ya no existe.
				param: [ Issue, Issue, ... ]
				return: [ Issue, Issue, Issue, ... ]
			*/
			function _cacheIssues(issues) {
				for (var i = 0; i < issues.length; i++) {
					var issue = issues[i];
					if ($window.sessionStorage.getItem(issue.id) == null) {
						$window.sessionStorage.setItem(issue.id, JSON.stringify(issue));
					}
				}
				return $q.when(issues);
			}

			/*
				Invalida la cache de los issues asignados a la persona y los que realizó.
			*/
			function _asyncInvalidateCache(issueId) {
				try {
					if ($window.sessionStorage.getItem('assignedIssues') != null) {
						$window.sessionStorage.removeItem('assignedIssues');
					}
					if ($window.sessionStorage.getItem('myIssues') != null) {
						$window.sessionStorage.removeItem('myIssues');
					}
					;
				} catch(err) {
					console.log(err);
				}
				return $q.when(issueId);
			}

			/*
				Invalida un issue en particular.
			*/
			function _asyncInvalidateSingleIssueCache(issue) {
				try {
					if ($window.sessionStorage.getItem(issue.id) != null) {
						$window.sessionStorage.removeItem(issue.id);
					}
				} catch(err) {
					console.log(err);
				}
				return $q.when(issue);
			}

			//////////////////////////////////


		}

})();

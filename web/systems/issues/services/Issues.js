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

		  function getMyIssues() {
				var myIssues = $window.sessionStorage.getItem('myIssues');
				if (myIssues != null) {
					var d = $q.defer();
					d.resolve(JSON.parse(myIssues));
					return d.promise;
				}

				return Login.getPrivateTransport().call('issues.get_my_issues').then(
					function(issues) {
						$window.sessionStorage.setItem('myIssues', JSON.stringify(issues));
						return issues;
					}
				);
			}

		  function getOfficesIssues() {
				return Login.getPrivateTransport().call('issues.get_offices_issues');
			}

		  function getAssignedIssues(statuses, froms, tos) {
				var assignedIssues = $window.sessionStorage.getItem('assignedIssues');
				if (assignedIssues != null) {
					var d = $q.defer();
					var ids = JSON.parse(assignedIssues);
					d.resolve(_loadIssues(ids));
					return d.promise;
				}


				return Login.getPrivateTransport().call('issues.get_assigned_issues', [statuses, froms, tos]).then(
					function(issues) {
						var ids = [];
						for (var i = 0; i< issues.length; i++) {
							var id = issues[i].id;
							ids.push(id);
							$window.sessionStorage.setItem(id, JSON.stringify(issues[i]));
						}
						$window.sessionStorage.setItem('assignedIssues', JSON.stringify(ids));
						return issues;
					}
				);
			}

			function updateIssue(id, status, priority) {
				var item = JSON.parse($window.sessionStorage.getItem(id));
				item.statusId = status;
				item.priority = priority;
				$window.sessionStorage.setItem(id, JSON.stringify(item));
			}

			function _loadIssues(ids) {
				var issues = [];
				for (var i = 0; i < ids.length; i++) {
					issues.push(JSON.parse($window.sessionStorage.getItem(ids[i])));
				}
				return issues;
			}

		  function findById(id) {
				return Login.getPrivateTransport().call('issues.find_by_id', [id]);
			}


			/*
				Solo sirve para invalidar la cache de los issues que existan.
			*/
			function _asyncInvalidateCache(issueId) {
				var d = $q.defer()
				$window.sessionStorage.removeItem('assignedIssues');
				$window.sessionStorage.removeItem('myIssues');
				d.resolve(issueId);
				return d.promise;
			}

			/*
				Invalida un issue sin invalidar la lista de todos los demas.
				se usa cuando se modifica un solo issue.
			*/
			function _asyncInvalidateSingleIssueCache(issue) {
				var d = $q.defer()
				$window.sessionStorage.removeItem(issue.id);
				d.resolve(issueId);
				return d.promise;
			}

		  function create(subject, description, parentId, officeId, fromOfficeId, authorId, files) {
				return Login.getPrivateTransport().call('issues.create', [subject, description, parentId, officeId, fromOfficeId, authorId, files]).then(_asyncInvalidateCache())
			}

		  function createComment(subject, description, parentId, officeId, files) {
				return Login.getPrivateTransport().call('issues.create_comment', [subject, description, parentId, officeId, files]).then(_asyncInvalidateCache());
			}

		  function changeStatus(issue, status) {
				return Login.getPrivateTransport().call('issues.change_status', [issue, status]).then(_asyncInvalidateSingleIssueCache());
			}

		  function changePriority(issue, priority) {
				return Login.getPrivateTransport().call('issues.change_priority', [issue, priority]).then(_asyncInvalidateSingleIssueCache());
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

		}

})();

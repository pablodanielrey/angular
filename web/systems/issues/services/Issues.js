(function() {
		'use strict'
		angular
			.module('issues')
			.service('Issues', Issues);

		Issues.inject = ['Login'];

		function Issues(Login) {

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
			this.$wamp = Login.getPrivateTransport();


			this.setTransport = function(wamp) {
				this.$wamp = (this.$wamp== null) ? wamp : this.$wamp;
			}

			function subscribe(event, func) {
				this.$wamp.subscribe(event, func);
			}

		  function searchUsers(regex) {
				return this.$wamp.call('issues.search_users', [regex]);
			}

		  function getMyIssues() {
				return this.$wamp.call('issues.get_my_issues');
			}

		  function getOfficesIssues() {
				return this.$wamp.call('issues.get_offices_issues');
			}

		  function getAssignedIssues() {
				return this.$wamp.call('issues.get_assigned_issues')
			}

		  function findById(id) {
				return this.$wamp.call('issues.find_by_id', [id]);
			}

		  function create(subject, description, parentId, officeId, fromOfficeId, authorId, files) {
				return this.$wamp.call('issues.create', [subject, description, parentId, officeId, fromOfficeId, authorId, files])
			}

		  function createComment(subject, description, parentId, officeId, files) {
				return this.$wamp.call('issues.create_comment', [subject, description, parentId, officeId, files])
			}

		  function changeStatus(issue, status) {
				return this.$wamp.call('issues.change_status', [issue, status]);
			}

		  function changePriority(issue, priority) {
				return this.$wamp.call('issues.change_priority', [issue, priority]);
			}

			function getOffices() {
				return this.$wamp.call('issues.get_offices',[]);
			}

			function getOfficeSubjects(officeId) {
				return this.$wamp.call('issues.get_office_subjects',[officeId]);
			}

			function getAreas(officeId) {
				return this.$wamp.call('issues.get_areas',[officeId]);
			}

		}

})();

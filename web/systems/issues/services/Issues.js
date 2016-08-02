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
			this.$wamp = Login.getTransport().private;

		  function getMyIssues() {
				return this.$wamp.call('issues.get_my_issues');
			}

		  function getOfficesIssues() {
				return this.$wamp.call('issues.getOfficesIssues');
			}

		  function getAssignedIssues() {
				return this.$wamp.call('issues.getAssignedIssues')
			}

		  function findById(id) {
				return this.$wamp.call('issues.findById', [id]);
			}

		  function create(subject, description, parentId, officeId, fromOfficeId, authorId, files) {
				return this.$wamp.call('issues.create', [subject, description, parentId, officeId, fromOfficeId, authorId, files])
			}

		  function createComment(subject, description, parentId, officeId, files) {
				return this.$wamp.call('issues.createComment', [subject, description, parentId, officeId, files])
			}

		  function changeStatus(issue, status) {
				return this.$wamp.call('issues.changeStatus', [issue, status]);
			}

		  function changePriority(issue, priority) {
				return this.$wamp.call('issues.changePriority', [issue, priority]);
			}

			function getOffices() {
				return this.$wamp.call('issues.getOffices',[]);

			}

			function getAreas(officeId) {
				return this.$wamp.call('issues.getAreas',[officeId]);
			}

		}

})();

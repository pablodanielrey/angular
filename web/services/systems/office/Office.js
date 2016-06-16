angular
	.module('mainApp')
	.service('Office',Office);

Office.inject = ['Utils','Session','$wamp'];

function Office (Utils, Session, $wamp) {

	this.getOfficesByUserRole = function (userId, tree, role) {
		return $wamp.call('office.getOfficesByUserRole',[userId, tree, role]);
	}

	this.getOfficesByUser = function (userId, tree) {
		return $wamp.call('office.getOfficesByUser',[userId, tree]);
	}

	this.findById = function (ids) {
		return $wamp.call('office.findById',[ids]);
	}

	this.getOfficesUsers = function (uid) {
		return $wamp.call('office.getOfficesUsers',[uid]);
	}

};

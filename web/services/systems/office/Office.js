angular
	.module('mainApp')
	.service('Office',Office);

Office.inject = ['Utils','Session','$wamp'];

function Office (Utils, Session, $wamp) {

	this.getOfficesByUserRole = function (userId, tree, role) {
		return $wamp.call('office.getOfficesByUserRole',[userId, tree, role]);
	}

	this.findById = function (ids) {
		return $wamp.call('office.findById',[ids]);
	}

};

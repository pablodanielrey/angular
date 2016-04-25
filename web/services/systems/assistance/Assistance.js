angular
	.module('mainApp')
	.service('Assistance',Assistance);

Assistance.inject = ['Utils','Session','$wamp'];

function Assistance (Utils, Session, $wamp) {


	this.getAssistanceData = function (userIds, start, end) {
		return $wamp.call('assistance.getAssistanceData',[userIds, start, end]);
	}


};

angular
	.module('mainApp')
	.service('Positions', Positions);

Positions.inject = ['$rootScope', '$wamp', 'Session']

function Positions($rootScope, $wamp, Session) {

	this.getPosition = function (userId) {
		return $wamp.call('positions.getPosition',[userId]);
	}

}


var app = angular.module('mainApp');

app.service('LaboralInsertion', function($wamp, Notifications) {

	this.downloadDatabase = function(cok,cerr) {
		$wamp.call('system.laboralInsertion.download')
			.then(function(res) {
				cok(res);
			},function(err) {
			  cerr(err);
			}
		);
	}

});

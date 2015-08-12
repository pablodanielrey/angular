
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

	this.find = function(userId, cok, cerr) {
		$wamp.call('system.laboralInsertion.find',[userId])
			.then(function(data) {
				cok(data);
			},function(err) {
			  cerr(err);
			}
		);
	}

	this.update = function(data, cok, cerr) {
		$wamp.call('system.laboralInsertion.update',[data])
			.then(function(res) {
				cok(res);
			},function(err) {
			  cerr(err);
			}
		);
	}

});

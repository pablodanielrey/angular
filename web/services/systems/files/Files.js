
var app = angular.module('mainApp');

app.service('Files', function($wamp, Notifications) {

	this.find = function(id, cok, cerr) {
		$wamp.call('system.files.find',[id])
			.then(function(data) {
				cok(data);
			},function(err) {
			  cerr(err);
			}
		);
	}

	this.upload = function(id, name, data, cok, cerr) {
		$wamp.call('system.files.upload',[id, name, data])
			.then(function(ok) {
				cok(ok);
			},function(err) {
			  cerr(err);
			}
		);
	}

});

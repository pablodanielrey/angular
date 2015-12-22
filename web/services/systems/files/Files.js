
var app = angular.module('mainApp');

app.service('Files', function($wamp, Notifications) {

	this.find = function(id, cok, cerr) {
		return $wamp.call('system.files.find',[id]);
	}

	this.upload = function(id, name, data, cok, cerr) {
		return $wamp.call('system.files.upload',[id, name, data]);
	}

});


var app = angular.module('mainApp');

app.service('Files', function($wamp, Notifications) {

	this.BASE64 = 'base64';
	this.BINARY = 'binary';

	this.find = function(id) {
		return $wamp.call('system.files.find',[id]);
	}

	this.upload = function(id, name, mimetype, codec, data) {
		return $wamp.call('system.files.upload',[id, name, mimetype, codec, data]);
	}

});

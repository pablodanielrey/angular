(function() {
		'use strict'

		var app = angular.module('files');

		app.service('Files', function() {
			this.BASE64 = 'base64';
			this.BINARY = 'binary';

			this.find = function(id) {
				return $wamp.call('system.files.find',[id]);
			}

			this.findMetaDataById = function(id) {
				return $wamp.call('system.files.findMetaDataById',[id]);
			}

			this.upload = function(id, name, mimetype, codec, data) {
				return $wamp.call('system.files.upload',[id, name, mimetype, codec, data]);
			}
		});

})();

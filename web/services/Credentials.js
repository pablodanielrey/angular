var app = angular.module('mainApp');

app.service('Credentials', ['$rootScope','$wamp',

  function($rootScope, $wamp) {

    /*
    info local del explorador para detectar errores
    */
    this.getLocalInfo = function() {
      var info = {
        'appCodeName': navigator.appCodeName,
        'appName': navigator.appName,
        'appVersion': navigator.appVersion,
        'cookieEnabled': navigator.cookieEnabled,
        'language': navigator.language,
        'onLine': navigator.onLine,
        'platform': navigator.platform,
        'product': navigator.product,
        'userAgent': navigator.userAgent
      };
      return info;
    }


    this.resetPassword = function(username, cok, cerr) {
      $wamp.call('system.password.generateResetPasswordHash', [username])
  		.then(function(hash) {
	       if (hash == null) {
  				cerr('');
  			} else {
  				cok(hash);
  			}
  		},function(err) {
  			cerr(err);
  		});
    }

    this.changePasswordWithHash = function(creds, hash, cok, cerr) {
      $wamp.call('system.password.changePasswordWithHash', [creds.username, creds.password, hash])
  		.then(function(ok) {
	       if (ok) {
           cok();
         } else {
  				cerr('');
  			}
  		},function(err) {
  			cerr(err);
  		});
    }

    this.changePassword = function(sid, creds, cok, cerr) {
      $wamp.call('system.password.changePassword', [sid, creds.username, creds.newPassword])
  		.then(function(ok) {
	       if (ok) {
           cok();
         } else {
  				cerr('');
  			}
  		},function(err) {
  			cerr(err);
  		});
    }

}])

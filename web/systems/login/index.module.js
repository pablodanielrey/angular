(function() {
  'use strict';

  angular
      .module('login',['users','ngRoute','ngCookies'])

/*
  angular
      .module('login',['ngRoute','ngCookies','vxWamp', 'files'])
      .provider('$wampPublic', function ($wampProvider) {
          var host = location.hostname;
          var options = {
              url: 'ws://' + host + ':80/ws',
              realm: 'public',
              prefix: '$wampPublic',
              authmethods: ['anonymous']
          };
          this.$get = function ($injector) {
              console.log('wampPublic injector');
              $wampProvider.init(options);
              return $injector.invoke($wampProvider.$get);
          };
      })
      .provider('$wampCore', function ($wampProvider) {
        var host = location.hostname;
        var options = {
            url: 'ws://' + host + ':80/ws',
              realm: 'core',
              prefix: '$wampCore',
              authmethods: ['ticket']
          };
          this.$get = function ($injector) {
              console.log('wampCore injector');
              $wampProvider.init(options);
              return $injector.invoke($wampProvider.$get);
          };
      })
*/
})();

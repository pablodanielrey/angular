(function() {
  'use strict';

  angular
      .module('login',['ngRoute','ngCookies','vxWamp'])
      .provider('$wampPublic', function ($wampProvider) {
          var host = location.hostname;
          var options = {
              url: 'ws://' + host + ':80',
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
            url: 'ws://' + host + ':80',
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

})();

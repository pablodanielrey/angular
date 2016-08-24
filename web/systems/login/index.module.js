(function() {
  'use strict';

  angular
      .module('login',['ngRoute','ngCookies','vxWamp'])
      .provider('$wampPublic, $location', function ($wampProvider, $location) {
          var host = $location.host();
          var options = {
              url: 'ws://' + host + ':8080',
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
      .provider('$wampCore, $location', function ($wampProvider, $location) {
        var host = $location.host();
        var options = {
            url: 'ws://' + host + ':8080',
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

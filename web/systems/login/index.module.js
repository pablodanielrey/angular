angular
    .module('login',['ngRoute','vxWamp'])
    .config(function($wampProvider) {
        var conn = {
          url: "ws://" + location.host + ":8080",
          realm: "core",
          authmethods: ['ticket']
        };
        $wampProvider.init(conn);
    })
    .provider('$wampPublic', function ($wampProvider) {
        var options = {
            url: 'ws://127.0.0.1:8080',
            realm: 'public',
            prefix: 'wampPublic',
            authmethods: ['anonymous']
        };
        this.$get = function ($injector) {
            $wampProvider.init(options);
            return $injector.invoke($wampProvider.$get);
        };
    })

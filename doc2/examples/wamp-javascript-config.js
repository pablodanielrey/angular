
/*
  referencias :
  https://github.com/voryx/angular-wamp
*/

/*
 forma tradicional de configurar la conexión wamp en javascript
 las opciones se configuran en el provider
*/
angular
    .module('mainApp',['ngRoute','vxWamp'])
    .config(function($wampProvider) {
        var conn = {
          url: "ws://" + location.host + ":8080",
          realm: "core"
        };
        $wampProvider.init(conn);
    });



/*
  otra forma podría ser usar una función definida en rootScope que retorne las opciones a configurar dentro del provider.
  hay que renombrar el wamp par poder definir un nuevo provider que se base en el provider original.
*/

angular
    .module('mainApp',['ngRoute','vxWamp'])
    .provider('$wamp1', function() {
        this.$get = ['$rootScope', '$wampProvider', '$injector', function($rootScope, $wampProvider, $injector) {
            if ($rootScope.getWampOptions != undefined) {
              var opts = $rootScope.getWampOptions();
              $wampProvider.init(opts);
            } else {
              var opts = {
                url: 'ws://127.0.0.1:8080',
                realm: 'public',
                prefix: 'wamp1',
                authmethods: ['anonymous']
              };
              $wampProvider.init(opts);
            }
            return $injector.invoke($wampProvider.$get);
        }];
    });


/*
  otra posible opción es configurar tantas conexiones wamp como alternativas de opciones tengamos.
  cada una con su provider diferente.
*/
angular
    .module('login',['ngRoute','vxWamp'])
    .provider('$wampPublic', function ($wampProvider) {
        var options = {
            url: 'ws://127.0.0.1:8080',
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
        var options = {
            url: 'ws://127.0.0.1:8080',
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


/*
  Para poder iniciar la conexion en caso de vistas que tengan ng-view
  se puede usar el evento disparado.
*/

$scope.$on('$viewContentLoaded', function() {
  $wamp.open();
});


/*
  En caso de que no exista ng-view se puede usar app.run de angular
*/
angular
  .module('login')
  .controller('IndexLoginCtrl',IndexLoginCtrl)
  .run(function($wampPublic) {
    console.log('abriendo conexion');
    $wampPublic.open();
  });

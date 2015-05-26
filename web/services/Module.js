

/**
 * Metodos comunes a todos los modulos
 * @param {type} param1
 * @param {type} param2
 */
app.service('Module', ["$window", "Notifications", "Profiles", "Session",  function($window, Notifications, Profiles, Session) {

  /**
   * Inicializacion de modulo
   * Se inicializan los parametros de session del modulo para aquellos casos que se necesite carga de la sesion
   * @returns {undefined}
   */
  this.load = function(){
    if (!Session.isLogged()){
      Notifications.message("Error: Sesion no definida");
      $window.location.href = "/#/logout";
    }
    var sessionUserId = Session.getCurrentSessionUserId();
    if(!sessionUserId){
      Notifications.message("Error: No esta definido el usuario logueado");
      $window.location.href = "/#/logout";
    }
  };
  
  /**
   * Autorizacion de modulo
   * Se inicializan los parametros de session del modulo y se verifican los "profiles"
   * @returns {undefined}
   */
  this.authorize = function(profiles){
    this.load();
    Profiles.checkAccess(Session.getSessionId(),profiles,
      function(ok) {
        if (ok !== 'granted') {
          Notifications.message("Acceso no autorizado");
          $window.location.href = "/#/logout";
        }
      },
      function (error) {
        Notifications.message(error);
      }
    );  
  };
  
  this.getSessionUserId = function(){
    return Session.getCurrentSessionUserId();
  };

}]);


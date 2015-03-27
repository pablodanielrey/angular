var app = angular.module('mainApp');

/**
 * Controlador utilizado para administrar "solicitudes de justificaciones" de una autoridad
 * A grandes rasgos podemos definir dos tipos de solicitudes de justificacion:
 *		Personal: Es la que realiza una persona para si mismo.
 *		Tercera: Es la que realiza una autoridad para un subordinado.
 * El objetivo del controlador es definir solicitudes a un subordinado. Actualmente la autoridad solo puede solicitar "horas extra"
 * El controlador debe identificar el usuario al cual se le va a definir la socicitud, el usuario es definido en otro controlador, se escucha el evento de seleccion de usuario
 */
app.controller('RequestAuthorityCtrl', function($scope, Assistance, Notifications) {
			
	
}

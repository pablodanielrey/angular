<?php
/**
* @package mautic_post_send
* @version 0.1
*/

$params2 = __DIR__ . '/oauth_token.txt';
if (file_exists($params2)) {
	echo "ya existen los tokens";
	exit;
}

// genero el archivo de parametros.

$params = __DIR__ . '/oauth_params.txt';
$settings = array();

if (!file_exists($params)) {

	// escribo un archivo de ejemplo de parámetros.
  $callback = "http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
	$settings = array(
	    'baseUrl'          => 'http://www.mautic.com.ar',				// Base URL of the Mautic instance
	    'version'          => 'OAuth1a', 												// Version of the OAuth can be OAuth2 or OAuth1a. OAuth2 is the default value.
	    'clientKey'        => 'hash generado en mautic', 				// Client/Consumer key from Mautic
	    'clientSecret'     => 'hash generado en mautic',  			// Client/Consumer secret key from Mautic
	    'callback'         => $callback									   			// Redirect URI/Callback URI for this script
	);
	file_put_contents($params, json_encode($settings));

} else {
	$settings = json_decode(file_get_contents($params), true);
}


// inicio todo el tema de autorización y autenticación

include __DIR__ . '/vendor/autoload.php';

use Mautic\Auth\ApiAuth;

session_start();

$initAuth = new ApiAuth();
$auth = $initAuth->newAuth($settings);

if ($auth->validateAccessToken()) {
    if ($auth->accessTokenUpdated()) {
        $accessTokenData = $auth->getAccessTokenData();
				file_put_contents($params2, json_encode($accessTokenData));
        echo(json_encode($accessTokenData));
    }
}

?>

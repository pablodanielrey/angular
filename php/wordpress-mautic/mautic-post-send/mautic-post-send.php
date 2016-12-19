<?php
/**
* @package mautic_post_send
* @version 0.1
*/
/*
Plugin Name: Mautic Post Send
Plugin URI:
Description: Plugin for sending emails with mautic whenever a post is updated.
Author: Pablo Daniel Rey
Version: 0.1
Author URI:
*/

include __DIR__ . '/vendor/autoload.php';

use Mautic\Auth\ApiAuth;
use Mautic\MauticApi;

function mautic_post_send_email( $post_id ) {

	// If this is just a revision, don't send the email.
	//if ( wp_is_post_revision( $post_id ) )
	//	return;

	$post_title = get_the_title( $post_id );
	$post_url = get_permalink( $post_id );
	$subject = 'Se ha actualizado un post';

	$message = "Se ha actualizado un post en el wordpress:\n\n";
	$message .= $post_title . ": " . $post_url;

	error_log('ejecute codigo de wp');

	try {

		$baseUrl = 'http://www.mautic.econo.unlp.edu.ar';
		$publicKey = '';
		$secretKey = '';

		$accessToken = '';
		$accessTokenSecret = '';

		// ApiAuth::initiate will accept an array of OAuth settings
		$settings = array(
		    'baseUrl'          => $baseUrl,       // Base URL of the Mautic instance
		    'version'          => 'OAuth1a', // Version of the OAuth can be OAuth2 or OAuth1a. OAuth2 is the default value.
		    'clientKey'        => $publicKey,       // Client/Consumer key from Mautic
  	    'clientSecret'     => $secretKey,       // Client/Consumer secret key from Mautic
		    'callback'         => '',        // Redirect URI/Callback URI for this script
				'accessToken'			 => $accessToken,
				'accessTokenSecret' => $accessTokenSecret
		);

		error_log('inicializo auth');
		// Initiate the auth object
		$initAuth = new ApiAuth();
		$auth = $initAuth->newAuth($settings);

		error_log('auth inicializada');
		$api = new MauticApi();
		$emailApi = $api->newApi('emails', $auth, $baseUrl);

		/*
		if ($auth->validateAccessToken()) {
		    if ($auth->accessTokenUpdated()) {
		        $accessTokenData = $auth->getAccessTokenData();

		        //error_log(json_encode($accessTokenData));
		    }
		}
		*/

		error_log('api inicializada');
		error_log(json_encode($emailApi->get(9)));


		error_log(json_encode($emailApi->send(9)));

		error_log('enviado');

	} catch (Exception $e) {
		error_log('error');
		error_log($e);
	}

	error_log('finalizo');

}

add_action( 'save_post', 'mautic_post_send_email' );

?>

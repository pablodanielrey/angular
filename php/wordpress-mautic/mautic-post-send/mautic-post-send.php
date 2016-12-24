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

session_start();

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

		$settings = json_decode(file_get_contents(__DIR__ . '/oauth_params.txt'), true);
		$settings2 = json_decode(file_get_contents(__DIR__ . '/oauth_token.txt'), true);

		$initAuth = new ApiAuth();
		$auth = $initAuth->newAuth($settings);
		$auth->setAccessTokenDetails($settings2);
		if ($auth->validateAccessToken()) {
		    if ($auth->accessTokenUpdated()) {
		        $accessTokenData = $auth->getAccessTokenData();
						file_put_contents(__DIR__ . '/oauth_token.txt', json_encode($accessTokenData));
		    }
		}

		$api = new MauticApi();
		$emailApi = $api->newApi('emails', $auth, settings['baseUrl']);

		echo(json_encode($emailApi->get(9)));


		error_log(json_encode($emailApi->send(9)));

		error_log('enviado');

	} catch (Exception $e) {
		error_log('error');
		error_log($e);
	}

}

add_action( 'save_post', 'mautic_post_send_email' );

?>

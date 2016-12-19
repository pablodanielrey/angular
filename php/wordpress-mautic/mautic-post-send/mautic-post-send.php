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

function mautic_post_send_email( $post_id ) {

	// If this is just a revision, don't send the email.
	//if ( wp_is_post_revision( $post_id ) )
	//	return;

	$post_title = get_the_title( $post_id );
	$post_url = get_permalink( $post_id );
	$subject = 'Se ha actualizado un post';

	$message = "Se ha actualizado un post en el wordpress:\n\n";
	$message .= $post_title . ": " . $post_url;

	// Send email to admin.
	wp_mail( 'ditesi@econo.unlp.edu.ar', $subject, $message );
}

add_action( 'save_post', 'mautic_post_send_email' );

?>

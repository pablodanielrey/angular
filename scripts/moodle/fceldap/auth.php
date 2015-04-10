<?php
require_once($CFG->libdir.'/authlib.php');

class auth_plugin_fceldap extends auth_plugin_base {


  function __construct() {
    $this->authtype = 'fceldap';

    foreach($this->userfields as $value) {
      $this->config->{'field_updatelocal_' . $value} = "onlogin";
      $this->config->{'field_lock_' . $value} = "unlockedifempty";
    }

  }


  /**
  * @override
  */
  function user_login($username, $password) {

    $conn = pg_connect("host=163.10.17.80 dbname=dcsys user=dcsys password=dcsys");
    try {
      $rs = pg_query_params($conn, "select user_id from credentials.user_password where lower(username) = $1 and password = $2", array($username,$password));
      if (!$rs) {
        pg_close($conn);
        return false;
      }

      $result = pg_fetch_all($rs);
      if (!$result) {
        pg_close($conn);
        return false;
      }

      if (sizeof($result) > 0) {

        // chequeo que tenga el usuario para au24
        $userid = $result[0]["user_id"];
        $rs = pg_query_params($conn, "select id from au24.users where id = $1",array($userid));
        if (!$rs) {
          pg_close($conn);
          return false;
        }

        $result = pg_fetch_all($rs);
        if (!$result) {
          pg_close($conn);
          return false;
        }

        if (sizeof($result) > 0) {
          pg_close($conn);
          return true;
        }
        
        pg_close($conn);
        return false;
      }

      fpg_close($conn);
      return false;

    } catch (Exception $e) {
      throw $e;

    }
  }


  function can_edit_profile(){
    return true;
  }

/*
  function edit_profile_url() {
    return "http://www.fce.econo.unlp.edu.ar";
  }
*/

  function is_internal() {
    return false;
  }

/*
  function can_change_password() {
    return true;
  }

  function change_password_url() {
    return "http://www.fce.econo.unlp.edu.ar";
  }
*/


  /**
  * Read user information from external database and returns it as array().
  * Function should return all information available. If you are saving
  * this information to moodle user-table you should honour synchronisation flags
  * Solo deben existir los campos que el moodle puede leer, si hay algun campo adicional se genera error
  *
  * @param string $username username
  *
  * @return mixed array with no magic quotes or false on error
  */
  function get_userinfo($username) {

    $conn = pg_connect("host=163.10.17.80 dbname=dcsys user=dcsys password=dcsys");
    try {
      $rs = pg_query_params($conn, "select user_id from credentials.user_password where lower(username) = $1", array($username));
      $result = pg_fetch_array($rs);
      $userid = $result["user_id"];

      $rs = pg_query_params($conn, "select dni,name,lastname,city,country from profile.users where id = $1", array($userid));
      $result = pg_fetch_array($rs);

      $data = array();
      $data["uid"] = $userid;
      $data["firstname"] = $result["name"];
      $data["lastname"] = $result["lastname"];
      $data["numero_documento"]  = $result["dni"];
      $data["idnumber"]  = $result["dni"];
      $data["country"]  = $result["country"];
      $data["city"]  = $result["city"];
      $data["email"] = null;

      $rs = pg_query_params($conn, "select email from profile.mails where user_id = $1", array($userid));
      $result = pg_fetch_all($rs);

      // me quedo con el mail de econo si existe, si no me quedo con alguno de los que tenga.
      for ($i = 0; $i < sizeof($result); $i++) {
        $email = $result[$i]["email"];
        $data["email"] = $email;
        if (strpos($email,"econo.unlp.edu.ar") !== FALSE) {
          break;
        }
      }

      // esto para permitir el logeo igual sin tener mail
      if ($data["email"] == null) {
        $data["email"] = "correo alternativo pendiente";
      }


      // chequeo si es estudiante y le asigno como idnumber el legajo
      $rs = pg_query_params($conn, "select student_number from students.users where id = $1", array($userid));
      $result = pg_fetch_all($rs);
      if (sizeof($result) > 0) {
        $data["idnumber"] = $result[0]["student_number"];
      }
      
      pg_close($conn);
      return $data;

    } catch (Exception $e) {
      pg_close($conn);
      throw $e;

    }

  }
  
  function is_synchronised_with_external() {
    return true;
  }





/*
  demas funciones que se pueden usar en un plugin de autentificacion
  ver documentacion de moodle.


  function user_authenticated_hook($user, $username, $password) {

  }

  function prelogout_hook() {

  }

  function user_update($olduser,$newuser) { }


  function user_exists($username) {
    // hay que chequear a ver si existe
  }


  function prevent_local_passwords() {
    return false;
  }

  function password_expire($username) {
    return 365;
  }


  function user_update_password($user, $newpassword) { }



  function user_delete($olduser) {  }

  function can_signup() {
    // resetting of internal password?
    return false;
  }

  function user_signup($user, $notify=true) { }

  function can_confirm() {
    return false;
  }

  function user_confirm($username, $confirmsecret) { }

  function sync_roles() { }

  function config_form($config, $err, $user_fields) { }

  function validate_form($form, $err) { }

  function process_config($config) { }

  function loginpage_hook() { }

  function logoutpage_hook() { }

  function can_be_manually_set() {
    return true;
  }

*/

}

?>

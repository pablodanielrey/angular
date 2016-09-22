<?php

ini_set("display_errors", "1");

require_once($CFG->libdir.'/authlib.php');
require_once($CFG->libdir.'/main/config/config.php');
require_once($CFG->libdir.'/main/class/dbaccess/LdapAccess.php');

class auth_plugin_fceldap extends auth_plugin_base {

	function __construct(){
        $this->authtype = 'fceldap';
		
		foreach($this->userfields as $key){
			$this->config->{'field_updatelocal_' . $key} = "onlogin";
			$this->config->{'field_lock_' . $key} = "unlockedifempty";
		}
	}

	/**
	 * Definir datos principales del usuario en formato moodle. Los datos principales son aquellos que deben existir obligatoriamente
	 * @param array $rowLdap
	 * @return array
	 * @throws Exception Si no existen datos principales
	 */
	protected function defineUserMainData(array $rowLdap){
		$error = array();
		$row = array();
	
		if(empty($rowLdap["uid"])) {
			array_push($error, "uid");
		} else {
			$row["uid"] = $rowLdap["uid"];
		}		
		
		if(empty($rowLdap["givenname"])) {
			array_push($error, "nombres");
		} else {
			$row["firstname"] = $rowLdap["givenname"];
		}

		if(empty($rowLdap["sn"])) {
			array_push($error, "apellidos");
		} else {
			$row["lastname"] = $rowLdap["sn"];
		}

		$row["email"]  = (isset($rowLdap["mail"])) ? $rowLdap["mail"] : null;
		if(empty($row["email"])) {
			if(empty($rowLdap["x-dcsys-mail"])) {
				array_push($error, "email");
			} else {
				$row["email"] = $rowLdap["x-dcsys-mail"];
			}
		}

		if(count($error)) throw new Exception("Datos principales no definidos: ". implode (", ", $error));
		
		return $row;
	}
		
	/**
	 * definir usuario
	 * @param array $row Datos extraidos del ldap
	 * @return array Datos del usuario redefinidos en un formato mas legible
	 * @throws Exception si los datos no estan correctamente definidos
	 */
	protected function defineUser(array $rowLdap){
		$row = $this->defineUserMainData($rowLdap);
		$row["legajo"] = (!empty($rowLdap["x-dcsys-legajo"])) ? $rowLdap["x-dcsys-legajo"] : null;
		$row["idnumber"]  = (isset($rowLdap["x-dcsys-legajo"])) ? $rowLdap["x-dcsys-legajo"] : null;		
		$row["numero_documento"]  = (isset($rowLdap["x-dcsys-dni"])) ? $rowLdap["x-dcsys-dni"] : null;
		$row["country"]  = (isset($rowLdap["co"])) ? $rowLdap["co"] : null;
		$row["city"]  = (isset($rowLdap["l"])) ? $rowLdap["l"] : null;
		$row["dn"] = $rowLdap["dn"];
		
		return $row;
	}

	
	/**
	 * autenticar usuario
	 * @param string $username
	 * @return array con los datos del usuario o false si la autenticacion fue incorrecta
	 * @throws Exception
	 */
	protected function queryUser(LdapAccess $ldap, $username){
		$base_dn = "ou=people,dc=econo";
		$filter= "(uid=$username)";

		$result = $ldap->query($base_dn, $filter);
		if(!$result) throw new Exception($ldap->error());
			
		if (!$ldap->numRows($result)) { 
			return false;
		}
			
		if ($ldap->numRows($result) > 1) { 
			throw new Exception ( "La busqueda de usuario retorno mas de un registro" );
		}

		if (!$ldap->numRows($result)) return false;
		if (!$ldap->numRows($result) > 1) throw new Exception("La busqueda por uid retorno mas de un resultado");

		return $ldap->fetchAssoc($result, 0);
	}
	
	protected function authorize($username, $password){
		$ldap = new LdapAccess(LDAP_SERVER);
		$ldap->connect();		
		try{		
			$return = true;
			
			$rowLdap = $this->queryUser($ldap, $username);
			
			if(!$rowLdap) $return = false;
			
			if($return){
				$row = $this->defineUser($rowLdap);
						
				$bind = $ldap->bind($row["dn"], $password);
				if(!$bind){
					$return = false;
				} else {
					$return = $row;
				}
			}
			
			$ldap->close();
			return $return;
		} catch (Exception $ex) {
			$ldap->close();
			throw $ex;
		}
	}
	
	/**
     * @override
     */
    function user_login($username, $password){
		$row = $this->authorize($username, $password);	
		if(!$row) return false;

		
		return true;
    }
    
    /**
     * @override
     */
    function can_edit_profile(){
    	return true;
    }
	
	/**
     * @override
     */
     function is_internal(){
     	return false;
     }

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
    function get_userinfo($username){
		$ldap = new LdapAccess(LDAP_SERVER);
		$ldap->connect();
		try{
			$return = true;

			$rowLdap = $this->queryUser($ldap, $username);
			if(!$rowLdap) $return = false;
			
			if($return){
				$return = $this->defineUser($rowLdap);
			}
				
			$ldap->close();
			
			return $return;
		} catch (Exception $ex) {
			$ldap->close();
			throw $ex;
		}
    }
	
	
	
}

?>


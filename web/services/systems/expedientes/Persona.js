
app.service("Persona", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.persona.findById', [id])
  }

  this.gridData = function(filterParams) {
    return $wamp.call('expedientes.persona.gridData', [filterParams])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.persona.numRows', [search])
  }


}]);
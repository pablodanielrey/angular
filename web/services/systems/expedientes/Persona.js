
app.service("Persona", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.persona.findById', [id])
  }

  this.gridData = function(search, pageSize, pageNumber) {
    return $wamp.call('expedientes.persona.gridData', [search, pageSize, pageNumber])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.persona.numRows', [search])
  }


}]);
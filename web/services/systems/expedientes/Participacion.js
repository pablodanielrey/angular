
app.service("Participacion", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.participacion.findById"', [id])
  }

  this.gridData = function(search, pageSize, pageNumber) {
    return $wamp.call('expedientes.participacion.gridData"', [search, pageSize, pageNumber])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.participacion.numRows"', [search])
  }


}]);
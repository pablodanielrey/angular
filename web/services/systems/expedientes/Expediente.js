
app.service("Expediente", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.expediente.findById', [id])
  }

  this.gridData = function(search, pageSize, pageNumber) {
    return $wamp.call('expedientes.expediente.gridData', [search, pageSize, pageNumber])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.expediente.numRows', [search])
  }


}]);

app.service("Lugar", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.lugar.findById"', [id])
  }

  this.gridData = function(search, pageSize, pageNumber) {
    return $wamp.call('expedientes.lugar.gridData"', [search, pageSize, pageNumber])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.lugar.numRows"', [search])
  }


}]);
app.factory('server', function($http) {
  return {
    getAssignments: function(id) {
      return $http.post('/assignments/' + id)
              .then(function(result) {
                return result.data;
              });
    }
  }
});

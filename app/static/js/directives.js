app.directive('focus', function($timeout) {
  return {
    scope: false,
    link: function(scope, element, attrs) {
      scope.$watch(attrs.focus, function(value) {
        if (value === true) {
          $timeout(function() {
              element[0].focus();
              scope[attrs.focus] = false;
          });
        }
      });
    }
  };
});

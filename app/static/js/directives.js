app.directive('focus', function($timeout) {
  return {
    scope: false,
    link: function(scope, element, attrs) {
      scope.$watch(attrs.focus, function(value) {
        console.log('value=', value);
        if (value === true) {
          $timeout(function() {
              element[0].focus();
              scope[attrs.focus] = false;
          });
        }
      });

      element.bind('blur', function() {
        //scope.$apply(model.assign(scope, false));
      });
    }
  };
});

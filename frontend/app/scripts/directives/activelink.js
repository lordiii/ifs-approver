'use strict';

/**
 * From http://jsfiddle.net/TheWoollyBully/qP58a/
 * @ngdoc directive
 * @name frontendApp.directive:activeLink
 * @description
 * # activeLink
 */
angular.module('frontendApp').directive('activeLink', function ($location) {
  return {
    restrict: 'A',
    link: function (scope, element, attrs) {
      var activeClass = attrs.activeLink;
      var path = attrs.ngHref || attrs.href;
      // remove first # if exist
      if (path.indexOf('#') === 0) {
        path = path.substring(1);
      }
      console.log('path', path);
      scope.location = $location;
      scope.$watch('location.path()', function (newPath) {
        console.log('new', newPath);
        if (path === newPath) {
          setTimeout(function () {
            element.addClass(activeClass);
          });
        } else {
          element.removeClass(activeClass);

          setTimeout(function () {
            scope.$apply(function () {
              scope.$eval(attrs.remove);
            });
          }, 200);
        }
      });
    }
  };
});

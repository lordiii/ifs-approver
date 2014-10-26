'use strict';

/**
 * @ngdoc directive
 * @description
 */
angular.module('frontendApp').directive('buttonWithComment', function ($timeout) {
  return {
    scope: {
      styleClass: '@',
      label: '@',
      action: '&'
    },
    transclude: true,
    templateUrl: 'views/buttonWithComment.tpl.html',
    restrict: 'EA',
    link: function postLink(scope, element, attrs) {
      scope.ui = {
        expand: false
      };

      scope.expand = function () {
        scope.ui.expand = true;
        scope.ui.comment = '';
        $timeout(function () {
          element.find('input')[0].focus();
        });
      };
      scope.cancel = function () {
        scope.ui.expand = false;
      };
      scope.submit = function () {
        scope.action({
          '$comment': scope.ui.comment
        });

        scope.ui.expand = false;
      };
    }
  };
});

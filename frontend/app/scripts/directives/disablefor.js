'use strict';

/**
 * @ngdoc directive
 * @name frontendApp.directive:disableFor
 * @description
 * # disableFor
 */
angular.module('frontendApp')
  .directive('disableFor', function () {
    return {
      scope: {
        isDisabled: '=disableFor'
      },
      restrict: 'A',
      link: function postLink(scope, element, attrs) {
        scope.$watch('isDisabled', function (newValue) {
          if (newValue) {
            element.attr('disabled', 'disabled');
          } else {
            element.removeAttr('disabled');
          }
        });
      }
    };
  });

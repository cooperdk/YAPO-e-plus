/*
** lazy-scroll v1.00
** (c) shabeeb
** mail@shabeebk.com
* shabeebk.com/blog/lazy-scroll-infinite-scrolling-angularjs
*
*/
angular.module("lazy-scroll",[])
        .directive('lazyScroll', [
                    '$rootScope',
                    '$window',
                    function($rootScope, $window) {
                    return {
                        link: function(scope, elem, attrs) {

                            var scrollEnabled, loadData, scrollTrigger = .90,scrollEnabled = true;;
                            $window = angular.element($window);
                            if (attrs.lazyNoScroll != null) {
                                 scope.$watch(attrs.lazyNoScroll, function(value) {
                                     scrollEnabled = (value == true) ? false : true;
                                 });
                            }

                            if ((attrs.lazyScrollTrigger != undefined) && (attrs.lazyScrollTrigger > 0 && attrs.lazyScrollTrigger <100) ) {
                                  scrollTrigger = attrs.lazyScrollTrigger/100;
                            }

                        loadData = function() {
                                var wintop = window.pageYOffset;
                                var docHeight = window.document.body.clientHeight;
                                var windowHeight = window.innerHeight//$window.height();
                                var triggered = (wintop/(docHeight - windowHeight));

                                if((scrollEnabled) && (triggered >= scrollTrigger) ){
                                     return scope.$apply(attrs.lazyScroll);
                                }
                            };

                            $window.on('scroll', loadData);
                            scope.$on('$destroy', function() {
                              return $window.off('scroll', loadData);
                            });
                          }
                    };
                   }
]);
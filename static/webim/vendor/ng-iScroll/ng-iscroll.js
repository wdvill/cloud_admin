angular.module('ng-iscroll', []).directive('ngIscroll', function() {
	return {
		replace: false,
		restrict: 'A',
		link: function(scope, element, attr){
			// default timeout
			var ngiScroll_timeout = 5;

			//获得 iscroll 的 名字
			var scroll_key = attr.ngIscroll;

			if (scroll_key === '') {
			  scroll_key = attr.id;
			}
			//获得scroll的选项
			var ngiScroll_opts = {
			  	snap: true,
			  	momentum: true,
			  	hScrollbar: false,
			  	mouseWheel: true,
			  	click: false,
			  	tap: true
		    };

			if (scope.$parent.myScrollOptions) {
			  for (var i in scope.$parent.myScrollOptions) {
				if(typeof(scope.$parent.myScrollOptions[i])!=="object"){
				  ngiScroll_opts[i] = scope.$parent.myScrollOptions[i];
				} else if (i === scroll_key) {
				  for (var k in scope.$parent.myScrollOptions[i]) {
					ngiScroll_opts[k] = scope.$parent.myScrollOptions[i][k];
				  }
				}
			  }
			}
			// iScroll initialize function
			function setScroll()
			{
			  if (scope.$parent.myScroll === undefined) {
				scope.$parent.myScroll = [];
			  }

			  scope.$parent.myScroll[scroll_key] = new iScroll(element[0], ngiScroll_opts);
			}
			// new specific setting for setting timeout using: ng-iscroll-timeout='{val}'
			if (attr.ngIscrollDelay !== undefined) {
			  ngiScroll_timeout = attr.ngIscrollDelay;
			}

			// watch for 'ng-iscroll' directive in html code
			scope.$watch(attr.ngIscroll, function ()
			{
			  setTimeout(setScroll, ngiScroll_timeout);
			});

			// add ng-iscroll-refresher for watching dynamic content inside iscroll
			if(attr.ngIscrollRefresher !== undefined) {
			  scope.$watch(attr.ngIscrollRefresher, function ()
			  {
				if(scope.$parent.myScroll[scroll_key] !== undefined) scope.$parent.myScroll[scroll_key].refresh();
			  });
			}

			// destroy the iscroll instance if we are moving away from a state to another
			// the DOM has changed and he only instance is not necessary any more
			scope.$on('$destroy', function () {
			  scope.$parent.myScroll[scroll_key].destroy();
			});

		}
	};
});

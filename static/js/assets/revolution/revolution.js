$(document).ready(function () {
    "use strict";
    
	//Revolution Slider
jQuery('#rev_slider_1').show().revolution({
		/* Options are 'auto', 'fullwidth' or 'fullscreen' */
		sliderLayout: 'false',
		gridwidth: 1140,
		gridheight: 870,
		/* Navigation arrows and bullets */
		navigation: {
			arrows: {
				enable: true,
				style: 'zeus',
				tmp: '<div class="tp-title-wrap"><div class="tp-arr-imgholder"></div></div>',
				hide_onleave: false,
				hide_onmobile: true,
				hide_under: 480
			}
		}
	});



});

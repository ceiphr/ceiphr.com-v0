// Materialize Init

$(document).ready(function () {
	$('.sidenav').sidenav();
	$('.tooltipped').tooltip();
	MathJax.Hub.Config({
		jax: ["input/TeX", "input/MathML", "input/AsciiMath", "output/CommonHTML"],
		extensions: ["tex2jax.js", "mml2jax.js", "asciimath2jax.js", "MathMenu.js", "MathZoom.js", "AssistiveMML.js", "a11y/accessibility-menu.js"],
		tex2jax: {
			inlineMath: [ ['$','$'], ["\\(","\\)"], ["\(","\)"]],
			displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
			processEscapes: true
		},
		TeX: {
			extensions: ["AMSmath.js", "AMSsymbols.js", "noErrors.js", "noUndefined.js"]
		}
	});
});
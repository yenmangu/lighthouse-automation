/**
 * @typedef {Object} IconBehaviour
 * @property {(svg:SVGElement) => void} onEnter
 * @property {(svg:SVGElement) => void} onLeave
 * @property {Record<string,any>} [prop]
 */

const RED = '#e84610ff';

/** @type {Map<string,IconBehaviour>} */
const ICON_BEHAVIOUR_MAP = new Map([
	[
		'comment_delete',
		{
			onEnter: svg => {
				setStrokeForAllPaths(svg, RED);
				setFill(svg, RED);
			},
			onLeave: svg => restoreOriginalStroke(svg)
		}
	],
	[
		'comment_edit',
		{
			onEnter: svg => setStrokeForAllPaths(svg, RED),
			onLeave: svg => restoreOriginalFill(svg)
		}
	]
	// Add more as app scales
]);

/**
 * @type {WeakMap<SVGElement,
 *	 {stroke:(string|null)[],
 *	 fill: (string|null)[]}>
 * }
 *
 */
const ORIGINAL_STYLE_MAP = new WeakMap();

(() => {
	// Narrow type
	const svgNodeList = /** @type {NodeListOf<SVGElement>} */ (
		document.querySelectorAll('svg[data_icon_key]')
	);

	// Quiet early return
	if (!svgNodeList.length) {
		return;
	}

	// SVG NodeList found
	svgNodeList.forEach(svg => {
		const iconKey = svg.getAttribute('data_icon_key');

		if (!iconKey) return;

		console.log('Found iconKey for: ', svg);

		const behaviour = ICON_BEHAVIOUR_MAP.get(iconKey);
		if (!behaviour) return;
		console.log('Found behaviour for: ', svg);

		cacheOriginalStyles(svg);

		svg.addEventListener('mouseenter', () => behaviour.onEnter(svg));
		svg.addEventListener('mouseleave', () => behaviour.onLeave(svg));
	});
})();

/**
 *
 * @param {SVGElement} svgEl
 * @param {string} colour
 */
function setStrokeForAllPaths(svgEl, colour) {
	const pathElements = svgEl.querySelectorAll('path');
	pathElements.forEach(path => {
		console.log('Setting stroke for path: ', path, ': ', colour);

		path.setAttribute('stroke', colour);
	});
}

/**
 *
 * @param {SVGElement} svgEl
 * @param {string} colour
 */
function setFill(svgEl, colour) {
	if (!svgEl.getAttribute('fill')) return;
	svgEl.setAttribute('fill', colour);
}

/**
 *
 * @param {SVGElement} svg
 */
function cacheOriginalStyles(svg) {
	console.log(`Running for: `, svg);

	if (ORIGINAL_STYLE_MAP.has(svg)) return;

	const paths = [...svg.querySelectorAll('path')];
	console.log('paths: ', paths);

	ORIGINAL_STYLE_MAP.set(svg, {
		stroke: paths.map(p => p.getAttribute('stroke')),
		fill: paths.map(p => p.getAttribute('fill`'))
	});

	console.log('Original style map: ', ORIGINAL_STYLE_MAP);
}

/**
 *
 * @param {SVGElement} svg
 */
function restoreOriginalStroke(svg) {
	const cached = ORIGINAL_STYLE_MAP.get(svg);
	if (!cached) return;

	const paths = svg.querySelectorAll('path');
	paths.forEach((path, i) => {
		const original = cached.stroke[i];
		if (original === null) {
			path.removeAttribute('stroke');
		} else {
			path.setAttribute('stroke', original);
		}
	});
}

/**
 *
 * @param {SVGElement} svg
 */
function restoreOriginalFill(svg) {
	const cached = ORIGINAL_STYLE_MAP.get(svg);
	if (!cached) return;

	const paths = svg.querySelectorAll('path');
	paths.forEach((path, i) => {
		const original = cached.fill[i];
		if (original === null) {
			path.removeAttribute('fill');
		} else {
			path.setAttribute('fill', original);
		}
	});
}

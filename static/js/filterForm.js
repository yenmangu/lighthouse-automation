/** @typedef {'mobile' | 'desktop'} FormPosition */

const DESKTOP_BREAKPOINT_PX = 992;

/** @type {FormPosition | null} */
let lastPosition = null;

const formRef = requireElementById('filterForm');
const desktopMount = requireElementById('desktopMount');
const mobileMount = requireElementById('mobileMount');

const offcanvasOpenButton = document.querySelector(
	"[data-bs-target='#filtersOffcanvas']"
);
if (offcanvasOpenButton) {
	offcanvasOpenButton.addEventListener('click', () => moveForm('mobile'));
}

function setInitialPlacement() {
	syncFormMountToViewport();
}

/**
 *
 * @param {string} id
 * @returns {HTMLElement}
 */
function requireElementById(id) {
	const element = document.getElementById(id);
	if (!element) {
		throw new Error(`Required element not found: #${id}`);
	}
	return element;
}

/**
 *
 * @returns {FormPosition}
 */
function getFormPositionForViewport() {
	return window.innerWidth < DESKTOP_BREAKPOINT_PX ? 'mobile' : 'desktop';
}

/**
 *
 * @param {FormPosition} position
 */
function moveForm(position) {
	const mount = position === 'desktop' ? desktopMount : mobileMount;
	mount.appendChild(formRef);
}

function syncFormMountToViewport() {
	const nextPosition = getFormPositionForViewport();
	if (nextPosition === lastPosition) return;
	lastPosition = nextPosition;
	moveForm(nextPosition);
}

setInitialPlacement();

window.addEventListener('resize', syncFormMountToViewport);

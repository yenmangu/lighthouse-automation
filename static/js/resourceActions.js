/**
 * @typedef {import('bootstrap')} Bootstrap
 */

const deleteButton = document.getElementById('resourceDelete');
const deleteModalRef = document.getElementById('deleteModal');

if (!deleteModalRef) {
	throw new Error('No delete modal found');
}

if (!deleteButton) {
	throw new Error('Delete button not found');
}

const deleteForm = deleteModalRef.querySelector('form');
if (!deleteForm) {
	throw new Error('Delete form not found');
}

const deleteModal = new bootstrap.Modal(deleteModalRef);

deleteButton.addEventListener('click', e => {
	const event = /** @type {MouseEvent} */ (e);
	const target = /** @type {HTMLElement} */ (event.currentTarget);
	if (!target.dataset.deleteUrl) {
		throw new Error('No delete url defined');
	}
	deleteForm.action = target.dataset.deleteUrl;
	deleteModal.show();
});

/**
 * @typedef {import('bootstrap')} Bootstrap
 */

const deleteButton = document.getElementById('resourceDelete');
const commentDeleteButtons =
	document.getElementsByClassName('btn-delete-comment');
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

const editBtns = document.getElementsByClassName('btn-edit-comment');
const commentText = document.getElementById('id_body');
const commentForm = /** @type {HTMLFormElement} */ (
	document.querySelector('form#commentForm')
);
const submitBtn = document.getElementById('submitButton');

if (!commentForm) {
	throw new Error('Comment form not found');
}
/**
 * Initialise edit functionality for the provided edit buttons
 *
 * For each button in the `editBtns` collection:
 * - Retrieves the associated comment's ID.
 * - Fetches the content of the corresponding comment.1
 * - Populates the `commentText` input/textarea with the
 * comment's content for editing.
 * - Updates the submit button's text to "Update".
 * - Sets the form's action attribute to the `edit_comment/{commentId} endpoint.
 */

for (let btn of editBtns) {
	btn.addEventListener('click', e => {
		if (!commentText || !submitBtn) {
			if (!commentText) console.log('No id_body');
			if (!submitBtn) console.log('No submitBtn');

			console.trace('error');

			return;
		}

		const event = /** @type {MouseEvent} */ (e);
		const target = /** @type {HTMLElement} */ (event.currentTarget);
		const commentId = target.getAttribute('data-comment-id');
		const editUrl = target.dataset.editUrl;
		if (!editUrl) {
			throw new Error('No edit url found in dataset');
		}

		const commentContent =
			document.getElementById(`comment${commentId}`)?.innerText ?? '';

		const commentInput = /** @type {HTMLInputElement} */ (commentText);
		commentInput.value = commentContent;
		submitBtn.innerText = 'Update';
		commentForm.action = editUrl;

		// (`edit_comment/${commentId}`);
	});
}

for (let btn of commentDeleteButtons) {
	btn.addEventListener('click', e => {
		const target = /** @type {HTMLElement} */ (e.currentTarget);
		const deleteUrl = target.dataset.deleteUrl;
		if (!deleteUrl) {
			throw new Error('No delete url provided');
		}
		const deleteModal = new bootstrap.Modal(deleteModalRef);
		deleteForm.action = deleteUrl;
		deleteModal.show();
	});
}

deleteButton.addEventListener('click', e => {
	const event = /** @type {MouseEvent} */ (e);
	const target = /** @type {HTMLElement} */ (event.currentTarget);
	const deleteModal = new bootstrap.Modal(deleteModalRef);

	if (!target.dataset.deleteUrl) {
		throw new Error('No delete url defined');
	}
	deleteForm.action = target.dataset.deleteUrl;
	deleteModal.show();
});

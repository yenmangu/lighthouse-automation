/**
 * P 2b2 - Writing html to file
 * Aims:
 * - Takes filepath, HTML string.
 * - Writes file to disk.
 *
 * Caveats
 * - No directory creation.
 * - validate filepath (non empty strings only.)
 * - validate html string (must be string , empty should be error)
 *
 */

import fs from 'node:fs/promises';

/**
 *
 * @param {string} filePath
 * @param {string} html
 * @return {Promise<void>}
 */
export async function writeHtmlReport(filePath, html) {
	if (typeof filePath !== 'string' || filePath.trim().length === 0) {
		throw new TypeError(
			'[writeHtmlReport]: File path must be non empty string'
		);
	}

	if (typeof html !== 'string') {
		throw new TypeError('[writeHtmlReport]: HTML must be type string');
	}
	if (html.trim().length === 0) {
		throw new Error('[writeHtmlReport]: HTML string is empty.');
	}

	await fs.writeFile(filePath, html, { encoding: 'utf-8' });
}

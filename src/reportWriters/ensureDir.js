/**
 * P 2b1 - ensureDir
 * A small helper that guarantees a directory exists
 * if exists - do nothing
 * if doesnt exist - create it (including parents)
 *
 * Caveats
 * fs.promises.mkdir (recursive = true)
 * - Do not swallow errors
 * -  platform safe - no hard coded slashes
 *
 */

import fs from 'node:fs/promises';

/**
 *
 * @param {string} dirPath
 * @return {Promise<void>}
 */
export async function ensureDir(dirPath) {
	if (typeof dirPath !== 'string' || dirPath.trim().length === 0) {
		throw new TypeError(
			'[ensureDir]: directory path must be a non-empty string.'
		);
	}

	await fs.mkdir(dirPath, { recursive: true });
}

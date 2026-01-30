/**
 * @typedef {Object} OutputPaths
 * @property {string} outputDir
 * @property {string} htmlPath
 * @property {string} jsonPath
 */

import path from 'node:path';

/**
 *
 * @param {Date} rawDate
 * @returns {string}
 */
function formatTimestamp(rawDate) {
	const year = rawDate.getFullYear();
	const month = String(rawDate.getMonth() + 1).padStart(2, '0');
	const day = String(rawDate.getDate()).padStart(2, '0');

	const hours = String(rawDate.getHours()).padStart(2, '0');
	const minutes = String(rawDate.getMinutes()).padStart(2, '0');
	const seconds = String(rawDate.getSeconds()).padStart(2, '0');

	return `${year}-${month}-${day}_${hours}-${minutes}-${seconds}`;
}

/**
 *
 * @param {{baseDir?:string, timestamp?:Date}} [options]
 * @returns {OutputPaths}
 */
export function createOutputPaths(options = {}) {
	const baseDir = options.baseDir ?? path.join(process.cwd(), 'reports');
	const timestamp = options.timestamp ?? new Date();
	const stamp = formatTimestamp(timestamp);
	const outputDir = path.join(baseDir, stamp);
	return {
		outputDir,
		htmlPath: path.join(outputDir, 'report.html'),
		jsonPath: path.join(outputDir, 'report.json')
	};
}

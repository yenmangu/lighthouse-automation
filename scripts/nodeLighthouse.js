/**
 * Phase 1
 * Problems
 * 1. Run Lighthouse without CLI
 * 2. Where does Chrome come into it
 * 3. How to connect Lighthouse to chrome?
 * 4. How to persist output?
 *
 * Solutions
 * 1. Use as library
 * - import
 * - pass url
 * - receive result object
 * -- Does not launch chrome automatically
 * -- Must provide a chrome debug port
 *
 * 2. Use chrome launcher
 * - start chrome
 * - capture assigned port
 * - hand port to Lighthouse
 * -- Port mismatch = silent failure or hang
 * -- Chrome must be fully started
 *
 * 4. Take report string and write using filesystem
 * -- output format matters
 * -- Large reports -> block writes
 *
 */

// 1.0 - ensure Node can run this file
// 1.1 - ensure output folder can be written to
// - `./documentation/lighthouse/reports/`
// -- need file system

import fs from 'node:fs';
import path from 'path';
import process from 'node:process';

const DEFAULT_URL = 'https://example.com';

/**
 *
 * @param {string} dirPath
 * @returns
 */
function ensureDirExists(dirPath) {
	if (fs.existsSync(dirPath)) {
		return;
	}
	fs.mkdirSync(dirPath, { recursive: true });
}
async function main() {
	const targetUrl = process.argv[2] ?? DEFAULT_URL;

	const outputDir = path.resolve(
		process.cwd(),
		'documentation',
		'lighthouse',
		'reports'
	);
	console.log('outputdir: ', outputDir);
	ensureDirExists(outputDir);

	console.log(`[Lighthouse-Runner] Target URL: ${targetUrl}`);
	console.log(`[Lighthouse-Runner] Next - run Lighthouse and save a report`);
}

main().catch(error => {
	console.error(`[Lighthouse-Runner] Failed: `, error);
	process.exitCode = 1;
});

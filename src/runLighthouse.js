/**
 * P1: Prove single lighthouse run works against a single url.
 * Must:
 * - open chrome
 * - run lighthouse
 * - tear down chrome at the end, cleanly.
 *
 * return result object:
 * - finalDisplayedUrl
 * - lhr (JSON)
 * - report (HTML string)
 */

import * as ChromeLauncher from 'chrome-launcher';
import lighthouse from 'lighthouse';

/**
 * Coordinate launching Chrome, running Lighthouse
 * @param {{url?:string, chromeFlags?: string[]}} options
 * @returns {Promise<{finalUrl:string, lhr:any, reportHtmlList: string[]}>}
 */
export async function runLighthouse(options = {}) {
	/** @type {any | null} */
	let chrome = null;
	let url = 'https://www.google.com';
	try {
		url = options.url ?? url;
		const chromeFlags = options.chromeFlags ?? ['--headless'];

		chrome = await launchChrome({ ...options, chromeFlags });
		// chrome -> lighthouse against url
		// return report
		const runnerResult = await lighthouse(url, {
			output: 'html',
			logLevel: 'info',
			port: chrome.port
		});

		if (!runnerResult) {
			throw new Error('RunnerResult not resolved');
		}

		const finalUrl = runnerResult.lhr.finalDisplayedUrl;

		if (!finalUrl) {
			// Hard stop
			throw new Error(
				'[RunnerResult]: finalDisplayedUrl missing - serious error has ocurred'
			);
		}

		// const reportHtml = runnerResult?.report;
		let reportHtmlList = [];
		if (!Array.isArray(runnerResult.report)) {
			reportHtmlList.push(runnerResult.report);
		} else {
			reportHtmlList = runnerResult.report;
		}

		return {
			finalUrl,
			lhr: runnerResult?.lhr,
			reportHtmlList
		};
	} catch (err) {
		console.error('[runLighthouse]: ', err);
		throw err;
	} finally {
		// tear down chrome
		if (chrome) await cleanup(chrome);
	}
}

/**
 *
 * @param {{url?:string, chromeFlags?:string[] }} opts
 * // TODO: Extract to type
 */
async function launchChrome(opts = {}) {
	try {
		const chrome = await ChromeLauncher.launch({ ...opts });

		// Prove a chrome instance spawned
		console.log(`Chrome debugging port running on ${chrome.port}`);

		return chrome;
	} catch (err) {
		throw err;
	}
}

/**
 *
 * @param {any} chrome
 */
async function cleanup(chrome) {
	try {
		console.log('Cleaning up chrome:');

		await chrome.kill();
	} catch (err) {
		throw err;
	}
}

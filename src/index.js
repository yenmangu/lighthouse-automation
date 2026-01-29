import { runLighthouse } from './runLighthouse.js';

async function main() {
	const targetUrl = process.argv[2];
	try {
		const result = await runLighthouse({
			url: targetUrl
		});
		console.log('Result from lighthouse: ', result.lhr);
		console.log('Report done for: ', result.finalUrl);
	} catch (err) {
		throw err;
	}
}
main().catch(error => {
	console.error(`[Lighthouse-Runner] Failed: `, error);
	process.exitCode = 1;
});

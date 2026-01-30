import { describe, test } from '@jest/globals';
import fs from 'node:fs/promises';
import path from 'node:path';
import { writeHtmlReport } from './writeHtmlReport.js';
import { ensureDir } from './ensureDir.js';

describe('writeHtmlReport', () => {
	const tempBaseDir = path.join(process.cwd(), 'tmp-writeHtmlReport');
	const tempHtmlFile = 'testHtml.html';
	const tempHtmlFilePath = path.join(tempBaseDir, tempHtmlFile);

	beforeEach(async () => {
		await ensureDir(tempBaseDir);
	});

	afterEach(async () => {
		await fs.rm(tempBaseDir, { recursive: true, force: true });
	});

	test('write html string to file', async () => {
		const html = `<html>Ok</html>`;
		await writeHtmlReport(tempHtmlFilePath, html);
		const stats = await fs.stat(tempHtmlFilePath);
		expect(stats.isFile()).toBe(true);
		const fileContents = await fs.readFile(tempHtmlFilePath, {
			encoding: 'utf-8'
		});
		expect(fileContents).toContain(html);
	});

	test('negative write', async () => {
		const html = `<html>Failure if seen</html>`;
		await expect(writeHtmlReport('', html)).rejects.toThrow(
			'[writeHtmlReport]: File path must be non empty string'
		);
	});
});

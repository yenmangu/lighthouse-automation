import { describe, test } from '@jest/globals';
import path from 'node:path';
import { createOutputPaths } from './createOutputPaths.js';
describe('createOutputPaths', () => {
	test('Test deterministic output paths from createOutputPaths', () => {
		const fixedDate = new Date(2026, 0, 29, 21, 55, 55);
		const stamp = '2026-01-29_21-55-55';
		const defaultBaseDir = path.join(process.cwd(), 'reports');
		const paths = createOutputPaths({ timestamp: fixedDate });
		const { htmlPath, jsonPath, outputDir } = paths;

		expect(outputDir).toBe(path.join(defaultBaseDir, stamp));
		expect(htmlPath).toBe(path.join(paths.outputDir, 'report.html'));
		expect(jsonPath).toBe(path.join(paths.outputDir, 'report.json'));
	});
});

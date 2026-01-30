import { describe, test } from '@jest/globals';
import fs from 'fs/promises';
import path from 'node:path';
import { ensureDir } from './ensureDir.js';

describe('ensureDir', () => {
	const tempDirString = 'temp-ensureDir';
	const tempBaseDir = path.join(process.cwd(), tempDirString);
	const nestedPath = path.join(tempBaseDir, 'a', 'b', 'c');

	afterEach(async () => {
		await fs.rm(tempBaseDir, { recursive: true, force: true });
	});

	test('nested directory path is created', async () => {
		await ensureDir(nestedPath);
		const stats = await fs.stat(nestedPath);
		expect(stats.isDirectory()).toBe(true);
	});

	test('does not fail if directory exists', async () => {
		await ensureDir(nestedPath);
		await ensureDir(nestedPath);

		const stats = await fs.stat(nestedPath);
		expect(stats.isDirectory()).toBe(true);
	});
});

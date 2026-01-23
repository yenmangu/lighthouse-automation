import { describe, expect, test } from '@jest/globals';
import { CLI_FLAGS, CLI_ARGS_MAP, ArgParser } from './argParser.js';

/**
 * TDD for P1, P2, and P3 of the ArgParser class.
 */

describe('Test early phases of ArgParser', () => {
	const argParser = new ArgParser(CLI_FLAGS, CLI_ARGS_MAP);
	const exampleUrl = 'https://example.com';

	test('P1: Positionals are stored', () => {
		const { positionals } = argParser.parse([exampleUrl]);
		expect(positionals).toContain(exampleUrl);
	});

	test('P1: knownFlags are stored', () => {
		const examplePath = './test/path/location';
		const { options, knownFlags, unknowns, positionals } = argParser.parse([
			exampleUrl,
			'--output',
			examplePath,
			'-q'
		]);

		expect(knownFlags).toContain('quick');
		expect(knownFlags).toContain('output');
	});
});

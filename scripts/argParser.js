const CLI_FLAGS = {
	output: ['-o', '--output'],
	readFile: ['-r', '--read-file'],
	quick: ['-q', '--quick']
	// Add more and maintain
};

/**
 * Keys derived from CLI_FLAGS
 * @typedef {keyof typeof CLI_FLAGS} FlagKey
 *
 * Value(s) passed to handlers (argv[i+1])
 * @typedef {string | string[] | boolean} FlagValue
 *
 * Handler function signature
 * @typedef {(value: FlagValue) => any} ArgHandler
 *
 * CLI entry metadata
 * @typedef {object} Meta
 * @property {boolean} takesNextValue
 * @property {boolean} [repeatable]
 *
 * Shape of a single CLI entry
 * Note: If no meta, takesNextValue = false
 * @typedef {object} CliArgEntry
 * @property {ArgHandler} handler
 * @property {Meta} [meta]
 *
 * @typedef {object} ParseResult
 * @property {Record<string, FlagValue>} options
 * @property {string[]} positionals
 *
 */

/**
 * @typedef {Record<FlagKey,CliArgEntry>} CliArgsMap
 */

/**
 * @type {CliArgsMap}
 */
const CLI_ARGS_MAP = {
	output: {
		/**
		 *
		 * @param {FlagValue} value
		 * @returns {any}
		 */
		handler: value => {
			return undefined;
		},
		meta: { takesNextValue: true }
	},
	readFile: {
		handler: value => {
			return undefined;
		},
		meta: { takesNextValue: true }
	},
	quick: {
		handler: value => {
			return undefined;
		}
	}
};

export class ArgParser {
	/**
	 *
	 * @param {Record<string, string[]>} cliFlags
	 * @param {CliArgsMap} cliArgsMap
	 */
	constructor(cliFlags, cliArgsMap) {
		this.cliFlags = cliFlags;
		this.cliArgsMap = cliArgsMap;

		/** @type {Map<string,string>} */
		this.aliasToKey = this.#buildAliasIndex(cliFlags);
	}

	/**
	 * Plan
	 *
	 * parse(argv) contract:
	 * walk through tokens left -> right
	 * route recognised flags to handlers
	 * collect 'positionals' (tokens that are not recognised flags)
	 * return a result object that I can trust
	 *
	 * Return shape intention:
	 * {
	 * 	options: parsedd flag values,
	 * 	positionals: tokens that are not recognised flags (ie, URL)
	 * }
	 *
	 * Caveats:
	 * - Ensure positionals are returned as well
	 * - No external work done here - ONLY parse the CLI arguments
	 *
	 * Build in stages:
	 *
	 *
	 * Phase 1
	 * - skeleton loop + positionals
	 * -- No flag handling!
	 *
	 * P1 return shape =
	 * {
	 * options : {},
	 * positionals: string[],
	 * unknowns: string[]
	 * }
	 *
	 * Note: Keeping unknown tokens for use in phase 2
	 *
	 *
	 *
	 *
	 *
	 * @param {string[]} argv
	 * @returns {{options:any, positionals:string[], unknowns:string[]}}
	 */
	parse(argv) {
		const options = {};

		/** @type {string[]} */
		const positionals = [];

		/** @type {string[]} */
		const unknowns = [];

		for (let i = 0; i < argv.length; i++) {
			const token = argv[i];
			if (!this.#looksLikeFlag(token)) {
				positionals.push(token);
			} else {
				unknowns.push(token);
			}
		}

		return { options, positionals, unknowns };
	}

	/**
	 *
	 * @param {Record<string, string[]>} cliFlags
	 * @returns
	 */
	#buildAliasIndex(cliFlags) {
		const aliasToKey = new Map();

		for (const [key, alias] of Object.entries(cliFlags)) {
			if (aliasToKey.has(alias)) {
				throw new Error(`Duplicate flag alias registered: ${alias}`);
			}
			aliasToKey.set(alias, key);
		}

		return aliasToKey;
	}

	/**
	 *
	 * @param {string} token
	 * @returns {string|null}
	 */
	#resolveKey(token) {
		return this.aliasToKey.get(token) ?? null;
	}

	/**
	 *
	 * @param {string} token
	 * @returns {boolean}
	 */
	#looksLikeFlag(token) {
		return token.startsWith('-') && this.aliasToKey.has(token);
	}
}

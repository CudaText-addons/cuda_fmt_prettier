"""Prettier formatter plugin for CudaText with cuda_fmt integration."""

import os
import subprocess
import json
import shutil
import cudatext as ct
from cuda_fmt import get_config_filename

# Platform detection
IS_WIN = os.name == 'nt'

# Plugin loaded
print("Prettier: Plugin initialized")

def _get_hidden_startupinfo():
    """Get startupinfo to hide console window on Windows."""
    if IS_WIN:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        return startupinfo
    return None

# Lexer to Prettier parser mapping
LEXER_TO_PARSER = {
    # JavaScript family
    'JavaScript': 'babel',
    'JavaScript Babel': 'babel-flow',
    'TypeScript': 'typescript',

    # Stylesheets
    'CSS': 'css',
    'SCSS': 'scss',
    'LESS': 'less',

    # Markup
    'HTML': 'html',
    'XML': 'html',
    'Markdown': 'markdown',
    'MDX': 'mdx',

    # Data formats
    'JSON': 'json',
    'YAML': 'yaml',

    # GraphQL (requires CudaText lexer support - future)
    'GraphQL': 'graphql',

    # Template engines (HTML-based)
    'HTML Handlebars': 'html',
    'HTML Laravel Blade': 'html',
    'HTML Django DTL': 'html',
    'Jinja2': 'html',
    'Twig': 'html',
    'Svelte': 'html',
    'Vue': 'vue',
    'Pug': 'pug',
    'Jade': 'pug'
}

# Default configuration structure
DEFAULT_CONFIG = {
    'prettier_path': '',
    '// prettier_path': 'Custom path to Prettier executable. Leave empty for auto-detection',

    'timeout_seconds': 10,
    '// timeout_seconds': 'Prettier subprocess timeout in seconds (default: 10)',

    'use_prettier_config_file': True,
    '// use_prettier_config_file': 'If true, uses .prettierrc from project. If false, uses options below',

    '// PRETTIER OPTIONS NOTE': 'https://prettier.io/docs/en/options.html (only used when use_prettier_config_file=false)',

    'prettier_options': {
        'printWidth': 80,
        '// printWidth': 'Line length (default: 80)',

        'tabWidth': 2,
        '// tabWidth': 'Spaces per indentation (default: 2)',

        'useTabs': False,
        '// useTabs': 'Use tabs instead of spaces (default: false)',

        'semi': True,
        '// semi': 'Add semicolons (default: true)',

        'singleQuote': False,
        '// singleQuote': 'Use single quotes (default: false)',

        'jsxSingleQuote': False,
        '// jsxSingleQuote': 'Single quotes in JSX (default: false)',

        'quoteProps': 'as-needed',
        '// quoteProps': 'Quote object properties: as-needed | consistent | preserve (default: as-needed)',

        'trailingComma': 'es5',
        '// trailingComma': 'Trailing commas: none | es5 | all (default: es5)',

        'bracketSpacing': True,
        '// bracketSpacing': 'Spaces in brackets (default: true)',

        'bracketSameLine': False,
        '// bracketSameLine': 'Put > on same line in HTML/JSX (default: false)',

        'arrowParens': 'always',
        '// arrowParens': 'Arrow function parens: avoid | always (default: always)',

        'proseWrap': 'preserve',
        '// proseWrap': 'Wrap prose: always | never | preserve (default: preserve)',

        'htmlWhitespaceSensitivity': 'css',
        '// htmlWhitespaceSensitivity': 'HTML whitespace: css | strict | ignore (default: css)',

        'vueIndentScriptAndStyle': False,
        '// vueIndentScriptAndStyle': 'Indent script/style in Vue (default: false)',

        'endOfLine': 'lf',
        '// endOfLine': 'Line ending: auto | lf | crlf | cr (default: lf)',

        'embeddedLanguageFormatting': 'auto',
        '// embeddedLanguageFormatting': 'Format embedded code: auto | off (default: auto)',

        'singleAttributePerLine': False,
        '// singleAttributePerLine': 'One attribute per line in HTML/JSX (default: false)',

        'objectWrap': 'preserve',
        '// objectWrap': 'Object wrap mode: preserve | collapse (default: preserve, v3.5.0+)',

        'experimentalTernaries': False,
        '// experimentalTernaries': 'Ternary formatting: false | true (default: false, v3.1.0+, experimental)',

        'insertPragma': False,
        '// insertPragma': 'Insert @format pragma (default: false)',

        'requirePragma': False,
        '// requirePragma': 'Only format files with pragma (default: false)',

        'rangeStart': 0,
        '// rangeStart': 'Format from byte offset (default: 0 = start of file)',

        'rangeEnd': 'Infinity',
        '// rangeEnd': 'Format to byte offset (default: Infinity = end of file)'
    }
}

def get_config_path():
    """Get configuration file path (portable-aware)."""

    # Try cuda_fmt first
    if config_path := get_config_filename('Prettier'):
        return config_path

    # Fallback: build path manually
    app_dir = ct.app_path(ct.APP_DIR_SETTINGS)
    return os.path.join(app_dir, 'cuda_fmt_prettier.json')

def _filter_comments(config_dict):
    """Remove comment keys (starting with //) from config dict."""
    return {k: v for k, v in config_dict.items() if not k.startswith('//')}

def load_config():
    """Load plugin configuration from JSON file."""
    import copy

    config_path = get_config_path()

    # Guard clause: no config path available
    if config_path is None:
        return _filter_comments(copy.deepcopy(DEFAULT_CONFIG))

    # Guard clause: config file doesn't exist - create it
    if not os.path.exists(config_path):
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=2)
            print("Prettier: Created default config file")
        except Exception as e:
            print(f"NOTE: Cannot create Prettier config: {e}")
        return _filter_comments(copy.deepcopy(DEFAULT_CONFIG))

    # Load and merge with defaults
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)

        # Deep copy defaults and filter comments
        config = _filter_comments(copy.deepcopy(DEFAULT_CONFIG))

        # Deep merge prettier_options if present
        if 'prettier_options' in user_config:
            user_options = _filter_comments(user_config['prettier_options'])
            config['prettier_options'].update(user_options)
            del user_config['prettier_options']

        # Merge top-level options (also filtered)
        user_config = _filter_comments(user_config)
        config.update(user_config)

        return config

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in Prettier config: {e}")
        return _filter_comments(copy.deepcopy(DEFAULT_CONFIG))
    except Exception as e:
        print(f"ERROR: Failed to load Prettier config: {e}")
        return _filter_comments(copy.deepcopy(DEFAULT_CONFIG))

def find_prettier_executable(config):
    """Locate Prettier executable in order of priority.

    Search order:
    1. Custom path from config
    2. CudaText tools folder (portable-aware)
    3. Local project node_modules
    4. Package manager executors (npx, yarn, pnpm, bun)
    5. Global PATH
    """
    # 1. Custom path in config
    if custom_path := config.get('prettier_path', '').strip():
        if os.path.exists(custom_path):
            print(f"Prettier: Using custom path: {custom_path}")
            return custom_path

    # 2. CudaText tools folder (portable-aware using APP_DIR_DATA)
    app_dir = ct.app_path(ct.APP_DIR_DATA)
    cudatext_root = os.path.dirname(app_dir)
    tools_dir = os.path.join(cudatext_root, 'tools', 'Prettier')

    # Windows: try both .exe and .cmd
    # Unix: try prettier
    if IS_WIN:
        for exe_name in ['prettier.exe', 'prettier.cmd']:
            bundled = os.path.join(tools_dir, exe_name)
            if os.path.isfile(bundled):
                print(f"Prettier: Using bundled version: {bundled}")
                return bundled
    else:
        bundled = os.path.join(tools_dir, 'prettier')
        if os.path.isfile(bundled):
            print(f"Prettier: Using bundled version: {bundled}")
            return bundled

    # 3. Local project installation
    cwd = os.getcwd()
    exe_suffix = '.cmd' if IS_WIN else ''
    local_prettier = os.path.join(cwd, 'node_modules', '.bin', f'prettier{exe_suffix}')

    if os.path.isfile(local_prettier):
        print(f"Prettier: Using local project installation: {local_prettier}")
        return local_prettier

    # 4. Package manager executors (space-separated for subprocess)
    package_managers = (
        ['npx.cmd prettier', 'yarn.cmd exec prettier', 'pnpm.cmd exec prettier', 'bunx.cmd prettier']
        if IS_WIN else
        ['npx prettier', 'yarn exec prettier', 'pnpm exec prettier', 'bunx prettier']
    )

    for pm_cmd in package_managers:
        try:
            cmd_parts = pm_cmd.split()
            result = subprocess.run(
                cmd_parts + ['--version'],
                capture_output=True,
                timeout=3,
                text=True,
                startupinfo=_get_hidden_startupinfo()
            )
            if result.returncode == 0:
                print(f"Prettier: Using package manager: {pm_cmd}")
                return pm_cmd
        except Exception:
            continue

    # 5. Global PATH
    if path := shutil.which('prettier'):
        print(f"Prettier: Found in PATH: {path}")
        return path

    print("NOTE: Prettier not found - install via npm/yarn/pnpm or configure path")
    return None

def build_prettier_command(prettier_path, parser, config):
    """Build Prettier command with all configured options."""
    # Handle package manager executors (contains spaces)
    cmd_parts = prettier_path.split() if ' ' in prettier_path else [prettier_path]

    # Required parser argument
    cmd_parts.extend(['--parser', parser])
    cmd_parts.append('--no-color')  # Disable ANSI color codes in output

    # Skip inline options if using project .prettierrc
    if config.get('use_prettier_config_file', True):
        print(f"Prettier: Command: {' '.join(cmd_parts)}")
        return cmd_parts

    # Build inline options from config
    options = config.get('prettier_options', {})

    # Print width and tabs
    if 'printWidth' in options:
        cmd_parts.extend(['--print-width', str(options['printWidth'])])
    if 'tabWidth' in options:
        cmd_parts.extend(['--tab-width', str(options['tabWidth'])])
    if options.get('useTabs', False):
        cmd_parts.append('--use-tabs')

    # Semicolons and quotes
    if not options.get('semi', True):
        cmd_parts.append('--no-semi')
    if options.get('singleQuote', False):
        cmd_parts.append('--single-quote')
    if options.get('jsxSingleQuote', False):
        cmd_parts.append('--jsx-single-quote')
    if 'quoteProps' in options:
        cmd_parts.extend(['--quote-props', options['quoteProps']])

    # Trailing commas and brackets
    if 'trailingComma' in options:
        cmd_parts.extend(['--trailing-comma', options['trailingComma']])
    if not options.get('bracketSpacing', True):
        cmd_parts.append('--no-bracket-spacing')
    if options.get('bracketSameLine', False):
        cmd_parts.append('--bracket-same-line')

    # Arrow functions and line endings
    if 'arrowParens' in options:
        cmd_parts.extend(['--arrow-parens', options['arrowParens']])
    if 'endOfLine' in options:
        cmd_parts.extend(['--end-of-line', options['endOfLine']])

    # Language-specific options
    if 'proseWrap' in options:
        cmd_parts.extend(['--prose-wrap', options['proseWrap']])
    if 'htmlWhitespaceSensitivity' in options:
        cmd_parts.extend(['--html-whitespace-sensitivity', options['htmlWhitespaceSensitivity']])
    if options.get('vueIndentScriptAndStyle', False):
        cmd_parts.append('--vue-indent-script-and-style')
    if 'embeddedLanguageFormatting' in options:
        cmd_parts.extend(['--embedded-language-formatting', options['embeddedLanguageFormatting']])

    # Advanced options
    if options.get('singleAttributePerLine', False):
        cmd_parts.append('--single-attribute-per-line')
    if 'objectWrap' in options:
        cmd_parts.extend(['--object-wrap', options['objectWrap']])
    if options.get('experimentalTernaries', False):
        cmd_parts.append('--experimental-ternaries')
    if options.get('insertPragma', False):
        cmd_parts.append('--insert-pragma')
    if options.get('requirePragma', False):
        cmd_parts.append('--require-pragma')

    # Range formatting (always explicit)
    range_start = options.get('rangeStart')
    range_end = options.get('rangeEnd')
    cmd_parts.extend(['--range-start', str(0 if range_start is None else range_start)])
    cmd_parts.extend(['--range-end', str('Infinity' if range_end is None else range_end)])

    print(f"Prettier: Command: {' '.join(cmd_parts)}")
    return cmd_parts

def do_format(text, lexer=''):
    """Format text using Prettier (called by cuda_fmt framework).

    cuda_fmt automatically handles line state preservation via difflib,
    so we just need to return the formatted text.

    Args:
        text: Source code to format
        lexer: CudaText lexer name (auto-detected if empty)

    Returns:
        Formatted text string, or None on error
    """
    # Guard clause: empty text
    if not text or not text.strip():
        return text  # Return as-is, nothing to format

    # Auto-detect lexer if not provided (cuda_fmt may pass empty string)
    if not lexer:
        lexer = ct.ed.get_prop(ct.PROP_LEXER_FILE)

    # Guard clause: unsupported lexer
    if not (parser := LEXER_TO_PARSER.get(lexer)):
        print(f'NOTE: Prettier does not support lexer "{lexer}"')
        return None

    # Load configuration
    config = load_config()

    # Guard clause: Prettier not found
    if not (prettier_path := find_prettier_executable(config)):
        return None

    # Build command
    cmd = build_prettier_command(prettier_path, parser, config)

    print(f"Prettier: Formatting with parser: {parser}")

    # Validate and get timeout
    timeout = config.get('timeout_seconds', 10)
    if not isinstance(timeout, (int, float)) or timeout <= 0:
        print(f"NOTE: Invalid timeout '{timeout}', using default: 10")
        timeout = 10

    try:
        # Get current file directory for .prettierrc discovery
        current_file = ct.ed.get_filename()
        cwd = os.path.dirname(current_file) if current_file else None

        # Execute Prettier via stdin/stdout
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
            startupinfo=_get_hidden_startupinfo()
        )

        stdout, stderr = process.communicate(input=text, timeout=timeout)

        # Guard clause: formatting failed
        if process.returncode != 0:
            error_msg = stderr.strip() if stderr else 'Unknown error'

            # Show syntax errors with context
            if 'SyntaxError' in error_msg or 'ParseError' in error_msg:
                lines = error_msg.split('\n')[:3]
                print(f'ERROR: Prettier syntax error:\n  ' + '\n  '.join(lines))
            else:
                print(f'ERROR: Prettier failed: {error_msg}')

            return None

        # Guard clause: empty output (shouldn't happen but defensive)
        if not stdout:
            print('ERROR: Prettier returned empty output')
            return None

        # Return formatted text
        # cuda_fmt will automatically preserve line states using difflib
        return stdout

    except subprocess.TimeoutExpired:
        print(f'ERROR: Prettier timed out (>{timeout}s)')
        return None

    except FileNotFoundError:
        print('ERROR: Prettier executable not found')
        return None

    except Exception as e:
        print(f'ERROR: Prettier execution failed: {e}')
        return None


class Command:
    """Command class for CudaText plugin system."""

    def config(self):
        """Open configuration file in editor."""

        config_path = get_config_path()

        # Guard clause: cannot determine config path
        if config_path is None:
            ct.msg_box('Cannot determine config path', ct.MB_OK | ct.MB_ICONERROR)
            return

        # Create config if doesn't exist
        if not os.path.exists(config_path):
            load_config()  # This will create the default config

        # Open in editor
        ct.file_open(config_path)

    def create_prettierrc(self):
        """Create .prettierrc file in the directory of the current file."""

        # Get current file path
        current_file = ct.ed.get_filename()

        # Guard clause: unsaved file (no directory to create .prettierrc in)
        if not current_file:
            ct.msg_box(
                'Cannot create .prettierrc:\n\n'
                'The current file has not been saved yet.\n'
                'Please save the file first or open an existing file to determine its directory.',
                ct.MB_OK | ct.MB_ICONWARNING
            )
            return

        # Get directory and path
        file_dir = os.path.dirname(current_file)
        prettierrc_path = os.path.join(file_dir, '.prettierrc')

        # Guard clause: already exists
        if os.path.exists(prettierrc_path):
            # Open in editor
            ct.file_open(prettierrc_path)
            return

        # Get filtered prettier options (no comments)
        import copy
        prettierrc_config = _filter_comments(copy.deepcopy(DEFAULT_CONFIG['prettier_options']))

        # Replace rangeEnd "Infinity" string with max int32 for .prettierrc compatibility
        if 'rangeEnd' in prettierrc_config:
            prettierrc_config['rangeEnd'] = 2147483647

        # Create file
        try:
            with open(prettierrc_path, 'w', encoding='utf-8') as f:
                json.dump(prettierrc_config, f, indent=2)

            print(f"Prettier: Created .prettierrc: {prettierrc_path}")

            # Open in editor
            ct.file_open(prettierrc_path)

        except Exception as e:
            print(f"NOTE: Cannot create .prettierrc: {e}")

    def help(self):
        """Display plugin help with version info."""

        # Try to get Prettier version
        version_info = ""
        config = load_config()
        if prettier_path := find_prettier_executable(config):
            try:
                # Get version (handle both single executable and package manager)
                cmd_parts = prettier_path.split() if ' ' in prettier_path else [prettier_path]
                result = subprocess.run(
                    cmd_parts + ['--version'],
                    capture_output=True,
                    timeout=3,
                    text=True,
                    startupinfo=_get_hidden_startupinfo()
                )
                if result.returncode == 0:
                    version = result.stdout.strip()
                    version_info = f"INSTALLED VERSION:\nPrettier {version}\n\n"
            except Exception:
                pass

        ct.msg_box(
            "Prettier Formatter for CudaText\n\n"
            "FEATURES:\n"
            "- Auto-detection (PATH, bundled, or project node_modules)\n"
            "- Support for 22 languages (JS, TS, JSON, CSS, HTML, templates, etc.)\n"
            "- Configurable options (17+ formatting rules)\n"
            "- Project .prettierrc support\n"
            "- Line state preservation (only modified lines marked)\n"
            "- Multi-platform (Windows, Linux, macOS)\n\n"
            "SUPPORTED LANGUAGES:\n"
            "JavaScript, JavaScript Babel (JSX), TypeScript, CSS, SCSS,\n"
            "LESS, HTML, XML, Markdown, MDX, JSON, YAML, GraphQL,\n"
            "HTML Handlebars, HTML Laravel Blade, HTML Django DTL,\n"
            "Jinja2, Twig, Svelte, Vue, Pug, Jade\n\n"
            "CONFIGURATION:\n"
            "Access via: Options > Settings-plugins > Prettier > Config\n"
            "- prettier_path: Custom path to Prettier executable\n"
            "- use_prettier_config_file: Use project .prettierrc (default: true)\n"
            "- prettier_options: Inline formatting options (used when above is false)\n"
            "- timeout_seconds: Subprocess timeout (default: 10)\n\n"
            "PROJECT CONFIG (recommended):\n"
            "Create .prettierrc in your project root with your preferred options.\n"
            "Plugin will automatically use it when use_prettier_config_file=true\n\n"
            "INSTALLATION METHODS:\n"
            "1. NPM (recommended):\n"
            "   npm install -g prettier\n"
            "2. Local project:\n"
            "   npm install --save-dev prettier\n"
            "3. Windows portable (.NET-based):\n"
            "   Download from nuget.org/packages/PackedPrettier\n"
            "   Place prettier.exe in CudaText/tools/Prettier/ (requires .NET)\n"
            "4. Windows portable (Node-based):\n"
            "   Install Node.js portable, run npm install -g prettier\n"
            "   Copy prettier.cmd to CudaText/tools/Prettier/\n"
            "5. Package managers:\n"
            "   yarn/pnpm/bun (auto-detected)\n\n"
            "USAGE:\n"
            "- Plugins > CudaFormatter > Formatter (menu)\n"
            "- Hotkey (optional): Install 'Configure_Hotkeys' plugin,\n"
            "  then search for 'CudaFormatter: Formatter (menu)'\n\n"
            f"{version_info}"
            "DOCUMENTATION:\n"
            "https://prettier.io/docs/",
            ct.MB_OK | ct.MB_ICONINFO
        )

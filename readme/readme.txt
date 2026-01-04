Formatter for CudaFormatter plugin.
It adds support for 22 languages: JavaScript, TypeScript, JSON, CSS, HTML, templates, and more.
It uses "Prettier".

'Prettier' must be in your system PATH, project node_modules, or in the tools/Prettier folder (portable use) inside CudaText directory.

Prettier is an opinionated code formatter:
https://prettier.io

Installation examples:
- NPM: npm install -g prettier
- Yarn: yarn global add prettier
- Windows portable (.NET-based): Download prettier.exe from https://www.nuget.org/packages/PackedPrettier and place it in tools/Prettier folder inside CudaText directory (requires .NET Runtime)
- Windows portable (Node-based): Install Node.js portable, run 'npm install -g prettier', copy prettier.cmd from node_modules\.bin\ to tools/Prettier folder
- Local project: npm install --save-dev prettier (auto-detected)

Access formatting via menu: Plugins > CudaFormatter > Formatter (menu)
Access global configuration via menu: Plugins > CudaFormatter > Configure formatter...
Access local configuration via menu: Plugins > CudaFormatter > Configure formatter (local)...
Access help via menu: Plugins > CudaFormatter > Formatter help...
Hotkey (optional): Install 'Configure_Hotkeys' plugin, then search for "CudaFormatter: Formatter (menu)"

Supported languages (22):
JavaScript, JavaScript Babel (JSX), TypeScript, CSS, SCSS, LESS,
HTML, XML, Markdown, MDX, JSON, YAML, GraphQL,
HTML Handlebars, HTML Laravel Blade, HTML Django DTL, Jinja2, Twig, Svelte,
Vue, Pug, Jade

Configuration modes:
1. Project config (recommended): Create .prettierrc in your project root
2. Plugin config: Edit settings/cuda_fmt_prettier.json

Example plugin config:
{
  "prettier_path": "",
  "timeout_seconds": 10,
  "use_prettier_config_file": true,
  "prettier_options": {
    "printWidth": 80,
    "tabWidth": 2,
    "singleQuote": false,
    "semi": true
  }
}

When use_prettier_config_file=true (default), Prettier searches for .prettierrc in your project.
When false, uses prettier_options from plugin config.

Author: Bruno Eduardo, https://github.com/Hanatarou

License: MIT

# CudaText plugin for Prettier code formatter

## 🎯 What is Prettier?

Prettier is an **opinionated code formatter** that enforces a consistent style across your entire codebase. It's the most popular code formatter in the JavaScript ecosystem and supports **19+ languages**:

- ✅ JavaScript, JSX, TypeScript
- ✅ JSON, YAML, GraphQL
- ✅ CSS, SCSS, LESS, Sass
- ✅ HTML, XML, Markdown
- ✅ Handlebars, Laravel Blade, Django, Jinja2, Twig, Svelte

Used by **millions of projects** including React, Vue, Angular, Babel, Webpack, and countless others.

## 📦 Installation

### Install the Plugin
1. In CudaText: **Plugins > Addon Manager > Install**
2. Search for "Prettier" and install

### Install Prettier
- **NPM (recommended)**: `npm install -g prettier`
- **Yarn**: `yarn global add prettier`
- **Windows portable**: Download `prettier.exe` from [PackedPrettier](https://www.nuget.org/packages/PackedPrettier) → place in `CudaText/tools/Prettier` folder (requires .NET Runtime)
- **Windows portable (Node-based)**: 
  1. Install Node.js portable
  2. `npm install -g prettier`
  3. Copy `prettier.cmd` from `node_modules\.bin\` to `CudaText/tools/Prettier`
- **Local project**: `npm install --save-dev prettier` (auto-detected)

Prettier must be in system PATH, project node_modules, or `CudaText/tools/Prettier` folder (portable mode).

## ✨ Plugin Features

### Core Functionality
- 🔌 **Full cuda_fmt integration** - Works seamlessly with CudaText formatter framework
- 🔍 **Smart executable detection** - Auto-finds Prettier in PATH, project, or bundled (portable mode)
- 📁 **Project config support** - Automatically reads `.prettierrc`, `.prettierrc.json`, `prettier.config.js`
- ⚙️ **JSON configuration** - Easy to configure with inline options or project config
- 🌍 **Cross-platform** - Windows, Linux, macOS fully supported
- 🔄 **Package manager support** - Auto-detects npx, yarn, pnpm, bun

### Advanced Features
- 🎨 **Line state preservation** - Only modified lines marked as changed (thanks to cuda_fmt difflib support)
- ↩️ **Single undo operation** - Format and undo with Ctrl+Z
- 🎯 **19 languages** - Comprehensive language support
- 📊 **Template engine support** - Formats Handlebars, Blade, Django, Jinja2, Twig, Svelte
- 🔧 **Flexible configuration** - Use project .prettierrc or plugin inline options
- 📝 **Debug logging** - Shows which executable and command used

### User Experience
- ⚡ **Fast formatting** - Prettier is highly optimized
- 🎯 **KISS principle** - Simple, clean code with minimal complexity
- 📦 **Portable-ready** - Works great with CudaText portable installations
- 🔄 **Live config reload** - Changes to config take effect immediately (no restart needed)

## 🚀 Usage

### Menu Commands
- **Plugins > CudaFormatter > Formatter (menu)** - Format current file
- **Options > Settings-plugins > Prettier > Config** - Configure options
- **Options > Settings-plugins > Prettier > Help** - Show help

### Hotkey (Optional)
1. Install **Configure_Hotkeys** plugin (via Addon Manager)
2. Search for **"CudaFormatter: Formatter (menu)"**
3. Assign your preferred hotkey (e.g., Shift+Alt+F)

### Configuration
Create `settings/cuda_fmt_prettier.json` to customize:
```json
{
  "prettier_path": "",
  "timeout_seconds": 10,
  "use_prettier_config_file": true,
  "prettier_options": {
    "printWidth": 80,
    "tabWidth": 2,
    "singleQuote": false,
    "semi": true,
    "trailingComma": "es5"
  }
}
```

**Recommended**: Use `.prettierrc` in your project root for team consistency:
```json
{
  "printWidth": 100,
  "singleQuote": true,
  "semi": false
}
```

## 📚 Additional Info
- **Prettier project**: https://github.com/prettier/prettier
- **Prettier documentation**: https://prettier.io/docs/
- **Author**: Bruno Eduardo, https://github.com/Hanatarou
- **License**: MIT

# Template Macros Organization

This directory contains reusable Jinja2 macros organized by category. These can be imported individually for better modularity and performance.

## Files

### `forms.html.jinja`
Form-related macros for building forms with Bootstrap 5 styling:
- `form_section()` - Complete form container with title and submit buttons
- `input_field()` - Text input field with label
- `select_field()` - Dropdown select field
- `textarea_field()` - Multi-line text input

### `tables.html.jinja`
Table-related macros for displaying data:
- `data_table()` - Responsive table with dark header
- `table_row()` - Clickable table row
- `action_buttons()` - Button group for row actions
- `table_form()` - Table with responsive card view for mobile

### `layout.html.jinja`
Page layout and structure macros:
- `page_header()` - Page title with subtitle and metadata

### `ui.html.jinja`
UI components like buttons, badges, and alerts:
- `flash_messages()` - Display Flask flash messages
- `alert_box()` - Alert component
- `empty_state()` - Empty state message
- `button_group()` - Horizontal button group
- `status_badge()` - Published/unpublished badge
- `ranking_badge()` - Ranking with medal icons

### `legacy.html.jinja`
Deprecated macros kept for backward compatibility:
- `form_card()` - Old-style centered form (use `form_section` instead)
- `form_input()` - Old-style input (use `input_field` instead)
- `form_select()` - Old-style select (use `select_field` instead)
- `table()` - Old-style table (use `data_table` instead)

## Usage

### Import from specific macro files (recommended)
```jinja
{% from "macros/forms.html.jinja" import input_field, select_field %}
{% from "macros/tables.html.jinja" import data_table, action_buttons %}
```

### Import from main macros file (backward compatibility)
```jinja
{% from "macros.html.jinja" import form_section, data_table %}
```

The main `macros.html.jinja` file includes all macros for backward compatibility with existing templates.

## Migration Guide

When updating old templates, prefer importing from specific macro files:

**Old:**
```jinja
{% from "macros.html.jinja" import form_input, form_select %}
```

**New:**
```jinja
{% from "macros/forms.html.jinja" import input_field, select_field %}
```

Also migrate from legacy macros to modern equivalents:
- `form_input` → `input_field`
- `form_select` → `select_field`
- `form_card` → `form_section`
- `table` → `data_table`

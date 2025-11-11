# AGENTS.md - AI Agent Documentation

## Project Context

This repository contains comprehensive BIOS documentation for the Machinist MD8 motherboard, created from 78 screenshots of the actual BIOS interface.

## Project Structure

```
machinist-MD8/
├── README.md              # User and developer documentation
├── AGENTS.md             # This file - AI agent guidelines
├── BIOS_MENU_MAP.md      # Complete BIOS menu tree mapping
└── fotos/                # Original BIOS screenshots (78 images)
    └── 20251109_*.jpg    # Screenshots in chronological order
```

## Key Information for AI Agents

### Project Purpose
- Document all menus, submenus, and options in the Machinist MD8 BIOS
- Provide reference mapping for BIOS navigation
- Serve as guide for system configuration

### Data Source
- 78 JPG screenshots taken from BIOS screen
- Screenshots follow chronological sequence
- Images with scrollbars show multiple pages (1st, 2nd, 3rd)
- Items with ">" indicate submenus
- Sequential images show submenu navigation depth

### BIOS Screen Layout
All BIOS screens are divided into 3 sections:
1. **Upper right block:** Description text
2. **Lower right block:** Command reference/hotkeys
3. **Left block:** Menu items and options (top to bottom)

### Main Menu Structure
```
1. Main - System info, date/time, SATA
2. Advanced - CPU, USB, network, serial, TPM
3. Chipset - System Agent, PCH-IO, graphics
4. Boot - Boot order and priorities
5. Security - Passwords and Secure Boot
6. Save & Exit - Save/discard options
```

### File Management Guidelines

#### When Editing Documentation
- Keep BIOS_MENU_MAP.md as single source of truth
- Maintain hierarchical structure with proper indentation
- Use consistent numbering scheme
- Preserve ">" markers for submenus
- Document all option values

#### When Adding Information
- Verify against original screenshots
- Maintain chronological order for images
- Update README.md if structure changes
- Keep AGENTS.md synchronized

### Code Style and Conventions

#### Markdown
- Use clear hierarchical headings (##, ###, ####)
- Maintain consistent list formatting
- Use code blocks for menu paths
- Use tables for structured data

#### Naming Conventions
- Menu items: Exact text from BIOS
- File names: Keep chronological timestamp format
- Variables: Descriptive, explicit names
- Comments: In English

### Technical Specifications

#### Motherboard: Machinist MD8
- **Chipset:** Intel
- **CPU:** Intel multi-core with Hyper-Threading
- **Memory:** DDR3/DDR4 support
- **Storage:** SATA (multiple ports), NVMe
- **Expansion:** PCIe Gen1/2/3
- **Features:** VT-x, VT-d, TPM 2.0, ME

### Common Tasks

#### Updating BIOS Documentation
1. Read relevant screenshot(s)
2. Verify menu path accuracy
3. Update BIOS_MENU_MAP.md
4. Maintain hierarchical structure
5. Document all available options

#### Adding New Information
1. Locate source screenshot
2. Extract menu/option data
3. Place in correct hierarchy
4. Verify option values
5. Update related sections

#### Searching for Specific Options
1. Use menu hierarchy in BIOS_MENU_MAP.md
2. Search by menu path (e.g., "Advanced > CPU Configuration")
3. Cross-reference with screenshots if needed
4. Verify option availability

### Validation Rules

#### Documentation Accuracy
- All options must match screenshots exactly
- Menu paths must reflect actual navigation
- Option values must be complete
- Descriptions must be clear and concise

#### Structural Integrity
- Maintain consistent indentation
- Number sections systematically
- Mark submenus with ">"
- Keep hotkey references accurate

### Common Pitfalls to Avoid

1. **Don't** invent options not visible in screenshots
2. **Don't** guess at menu structures
3. **Don't** modify chronological order of images
4. **Don't** remove ">" indicators from submenus
5. **Don't** add unnecessary complexity to documentation

### Best Practices

1. **Verify first:** Always check screenshots before documenting
2. **Stay organized:** Maintain strict hierarchical structure
3. **Be explicit:** Use full menu paths when referencing options
4. **Stay current:** Update documentation when new screenshots added
5. **Cross-reference:** Link related options across menus

### Dependencies and Tools

- **Image Format:** JPG (screenshots)
- **Documentation Format:** Markdown (.md)
- **Version Control:** Git
- **No external dependencies**

### Testing and Verification

#### When Updating Documentation
1. Verify menu path exists in BIOS
2. Check all option values are listed
3. Confirm submenu indicators
4. Validate hotkey references
5. Review for consistency

#### Quality Checks
- Spelling and grammar in English
- Consistent formatting throughout
- All submenus properly nested
- No broken references
- Clear and concise descriptions

### Language and Communication

- **Code/Documentation:** English only
- **Responses to user:** Portuguese (as per user rules)
- **Technical terms:** Keep original English terms
- **Comments:** Clear and descriptive

### Special Considerations

#### BIOS Screenshots
- Images are large (16K-24K lines when read as text)
- Don't re-read entire images unnecessarily
- Use grep/search when looking for specific content
- Reference by filename when discussing specific screens

#### Menu Navigation
- Follow chronological order of screenshots
- Track menu depth by ">" indicators
- Note scrollable sections (multiple screenshots)
- Document keyboard shortcuts

### Security and Safety

⚠️ **IMPORTANT:**
- BIOS settings can affect system stability
- Document warnings for critical options
- Note default values where applicable
- Indicate when restart required

### Future Enhancements

Potential areas for expansion:
- Cross-references between related options
- Default value documentation
- Hardware compatibility notes
- Common configuration scenarios
- Troubleshooting guide

---

## Quick Reference for AI Agents

### File Roles
- `README.md` - User-facing documentation
- `AGENTS.md` - This file, for AI agents
- `BIOS_MENU_MAP.md` - Complete BIOS structure
- `fotos/*.jpg` - Source screenshots

### Key Commands
- Read screenshot: Use read_file on specific image
- Search menu: Use grep on BIOS_MENU_MAP.md
- Update docs: Use search_replace or write

### Critical Rules
1. Always verify against screenshots
2. Maintain hierarchy strictly
3. Document all options completely
4. Use English for code/docs
5. Respond to user in Portuguese

---

**Last Updated:** 2025-11-09
**Version:** 1.0
**Maintainer:** AI Assistant Team


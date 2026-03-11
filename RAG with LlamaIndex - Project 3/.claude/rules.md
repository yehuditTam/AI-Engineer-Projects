# UI Development Rules

## RTL Support (Hebrew)
- **MANDATORY**: Every component MUST support RTL layout
- Use `dir="rtl"` on root elements
- Apply `text-right` for text alignment
- Mirror padding/margin: `pr-4` instead of `pl-4`
- Test all components in Hebrew before deployment

## Brand Colors (STRICT)
- **Deep Blue**: `#003366` - Primary color for headers, buttons, links
- **Gold**: `#D4AF37` - Accent color for highlights, hover states, CTAs
- **NO OTHER COLORS** allowed without explicit approval
- Use Tailwind config to enforce:
  ```
  colors: {
    brand: {
      blue: '#003366',
      gold: '#D4AF37'
    }
  }
  ```

## Form Styling
- **ABSOLUTE BAN** on external form libraries (React Hook Form, Formik, etc.)
- Build all forms with native HTML + custom styling
- Use controlled components with React state
- Manual validation logic only

---
*Enforced by Claude Code Agent*

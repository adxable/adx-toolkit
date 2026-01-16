---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when building web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
---

# Frontend Design

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## When to Use This Skill

- Building new UI components or pages
- Improving visual design quality
- Creating memorable user interfaces
- Avoiding generic, template-like designs

---

## Design Thinking

Before coding, understand the context and commit to a **BOLD aesthetic direction**:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

---

## Frontend Aesthetics Guidelines

### Typography

Choose fonts that are beautiful, unique, and interesting:
- Avoid generic fonts like Arial and Inter
- Opt for distinctive choices that elevate the frontend's aesthetics
- Use unexpected, characterful font choices
- Pair a distinctive display font with a refined body font

### Color & Theme

Commit to a cohesive aesthetic:
- Use CSS variables for consistency
- Dominant colors with sharp accents outperform timid, evenly-distributed palettes
- Don't be afraid of bold color choices when appropriate

### Motion

Use animations for effects and micro-interactions:
- Prioritize CSS-only solutions for HTML
- Use Motion library for React when available
- Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions
- Use scroll-triggering and hover states that surprise

### Spatial Composition

Think beyond standard layouts:
- Unexpected layouts
- Asymmetry
- Overlap
- Diagonal flow
- Grid-breaking elements
- Generous negative space OR controlled density

### Backgrounds & Visual Details

Create atmosphere and depth:
- Don't default to solid colors
- Add contextual effects and textures that match the overall aesthetic
- Apply creative forms like:
  - Gradient meshes
  - Noise textures
  - Geometric patterns
  - Layered transparencies
  - Dramatic shadows
  - Decorative borders
  - Custom cursors
  - Grain overlays

---

## What to AVOID

**NEVER use generic AI-generated aesthetics:**

- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

---

## Design Principles

### Interpret Creatively

Make unexpected choices that feel genuinely designed for the context:
- No design should be the same
- Vary between light and dark themes
- Use different fonts for different projects
- NEVER converge on common choices across implementations

### Match Complexity to Vision

- **Maximalist designs** need elaborate code with extensive animations and effects
- **Minimalist designs** need restraint, precision, and careful attention to spacing, typography, and subtle details
- Elegance comes from executing the vision well

### Be Bold

Don't hold back. Show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

---

## Quick Examples

### Brutalist/Raw
```css
.card {
  border: 3px solid black;
  box-shadow: 8px 8px 0 black;
  background: #fff;
  font-family: 'Courier New', monospace;
}
```

### Soft/Pastel
```css
.card {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(252, 182, 159, 0.3);
  font-family: 'Quicksand', sans-serif;
}
```

### Luxury/Refined
```css
.card {
  background: #0a0a0a;
  border: 1px solid rgba(255, 215, 0, 0.2);
  font-family: 'Playfair Display', serif;
  letter-spacing: 0.05em;
}
```

### Retro-Futuristic
```css
.card {
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
  border: 1px solid #0f4c75;
  box-shadow: 0 0 30px rgba(15, 76, 117, 0.5);
  font-family: 'Orbitron', sans-serif;
}
```

---

## Remember

Claude is capable of extraordinary creative work. The goal is to create interfaces that are memorable, functional, and distinctively designed - not generic templates that could come from any source.

# 🧬 PRIME UI - Complete Visual Design Blueprint

## 1. COLOR PALETTE

### Primary Colors
```
--prime-deep-space: #0a0e27
--prime-void-black: #080b1a
--prime-midnight: #111827
```

### Neon Accent Colors
```
--neon-cyan: #00fff9
--neon-purple: #bf00ff
--neon-pink: #ff00e5
--neon-blue: #0066ff
--electric-violet: #8b00ff
```

### Functional Colors
```
--glass-white: rgba(255, 255, 255, 0.05)
--glass-border: rgba(255, 255, 255, 0.1)
--glow-cyan: rgba(0, 255, 249, 0.3)
--glow-purple: rgba(191, 0, 255, 0.3)
```

## 2. TYPOGRAPHY

### Font Stack
```
Primary: 'Orbitron', 'Rajdhani', 'Space Grotesk', sans-serif
Secondary: 'Inter', 'system-ui', sans-serif
Mono: 'Fira Code', 'JetBrains Mono', monospace
```

### Type Scale
```
--text-xs: 0.75rem (12px)
--text-sm: 0.875rem (14px)
--text-base: 1rem (16px)
--text-lg: 1.125rem (18px)
--text-xl: 1.25rem (20px)
--text-2xl: 1.5rem (24px)
--text-3xl: 1.875rem (30px)
--text-4xl: 2.25rem (36px)
```

## 3. EFFECTS & ANIMATIONS

### Glassmorphism
```
background: rgba(255, 255, 255, 0.05)
backdrop-filter: blur(10px)
border: 1px solid rgba(255, 255, 255, 0.1)
box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37)
```

### Neon Glow
```
text-shadow: 0 0 10px currentColor, 0 0 20px currentColor
box-shadow: 0 0 15px var(--neon-cyan), 0 0 30px var(--neon-cyan)
```

### Holographic Border
```
border-image: linear-gradient(45deg, #00fff9, #bf00ff, #ff00e5, #00fff9) 1
animation: border-flow 3s linear infinite
```

### Transitions
```
Default: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)
Smooth: all 0.5s cubic-bezier(0.16, 1, 0.3, 1)
Bounce: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)
```

## 4. COMPONENT SPECIFICATIONS

### Buttons
- **Primary**: Glass bg + neon cyan border + glow on hover
- **Secondary**: Transparent + holographic border
- **Size**: 44px min height (touch-friendly)
- **Border Radius**: 8px
- **Hover**: Scale(1.02) + increased glow
- **Active**: Scale(0.98)

### Input Fields
- **Background**: Glass effect
- **Border**: 1px solid glass-border, neon on focus
- **Padding**: 12px 16px
- **Glow**: Cyan glow on focus
- **Placeholder**: rgba(255, 255, 255, 0.3)

### Cards
- **Background**: Glassmorphism
- **Border**: Holographic animated border
- **Padding**: 24px
- **Hover**: Lift effect (translateY(-4px)) + enhanced glow
- **Shadow**: Multi-layer neon shadow

### Progress Bars
- **Track**: Glass bg
- **Fill**: Gradient (cyan → purple)
- **Animation**: Shimmer effect
- **Height**: 4px
- **Border Radius**: 2px

## 5. LAYOUT GRID

### Spacing Scale
```
--space-1: 4px
--space-2: 8px
--space-3: 12px
--space-4: 16px
--space-6: 24px
--space-8: 32px
--space-12: 48px
--space-16: 64px
```

### Container Widths
```
--container-sm: 640px
--container-md: 768px
--container-lg: 1024px
--container-xl: 1280px
--container-2xl: 1536px
```

### Breakpoints
```
mobile: 640px
tablet: 768px
desktop: 1024px
wide: 1280px
```

## 6. ICONOGRAPHY

### Style
- **Type**: Outline icons with neon stroke
- **Weight**: 2px stroke
- **Size**: 20px, 24px, 32px
- **Hover**: Glow + slight rotation
- **Library**: Lucide Icons / Heroicons

## 7. BACKGROUND EFFECTS

### Particle System
- Small cyan/purple dots
- Slow floating animation
- Blur effect
- Opacity: 0.1-0.3

### Grid Overlay
- Perspective grid lines
- Fading to horizon
- Color: rgba(0, 255, 249, 0.05)
- Animation: Slow pulse

### Gradient Mesh
- Radial gradients from corners
- Colors: cyan, purple, blue
- Blur: 100px+
- Opacity: 0.15
- Animation: Slow rotation

## 8. INTERACTION STATES

### Hover
- Scale: 1.02
- Shadow: Enhanced glow
- Brightness: 110%
- Transition: 0.3s

### Active/Pressed
- Scale: 0.98
- Brightness: 95%
- Transition: 0.1s

### Focus
- Border: Neon cyan 2px
- Glow: Large cyan shadow
- Outline: None

### Disabled
- Opacity: 0.4
- Cursor: not-allowed
- Filter: grayscale(100%)

## 9. MOTION DESIGN

### Page Transitions
- Duration: 0.6s
- Easing: cubic-bezier(0.16, 1, 0.3, 1)
- Type: Fade + slight scale

### Tab Switching
- Duration: 0.4s
- Effect: Slide + fade
- Indicator: Animated underline

### Loading States
- Spinner: Neon gradient ring
- Skeleton: Shimmer animation
- Progress: Wave effect

### Micro-interactions
- Button ripple: 0.6s
- Icon pulse: 2s loop
- Tooltip appear: 0.2s
- Menu slide: 0.3s

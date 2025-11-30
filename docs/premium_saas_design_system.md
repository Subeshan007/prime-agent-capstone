# Premium SaaS Design System (PRIME Vercel/Stripe Style)

## 1. Color System

### Primary Palette
- **Background**: `#111315` (Deep Dark)
- **Surface Light**: `#1A1C1E` (Cards, Sidebar)
- **Surface Dark**: `#191B1D` (Inputs, Secondary)
- **Border**: `#2A2D30` (Subtle)
- **Accent**: `#3A7BFA` (Professional Blue)

### Functional Colors
- **Success**: `#2ECC71`
- **Warning**: `#F1C40F`
- **Error**: `#E74C3C`
- **Text Primary**: `#FFFFFF`
- **Text Neutral**: `#D7DADC`

## 2. Typography
**Font Family**: Inter, IBM Plex Sans, system-ui

| Style | Size | Weight | Line Height |
|-------|------|--------|-------------|
| H1    | 32px | 600    | 1.2         |
| H2    | 24px | 600    | 1.3         |
| Body  | 14px | 400    | 1.5         |
| Small | 12px | 400    | 1.5         |

## 3. Component Rules

### Cards
- **Background**: `#1A1C1E`
- **Border**: 1px solid `#2A2D30`
- **Radius**: 12px
- **Shadow**: `0 4px 6px -1px rgba(0, 0, 0, 0.1)`
- **Padding**: 24px

### Buttons
- **Primary**:
  - Bg: `linear-gradient(180deg, #3A7BFA 0%, #2A6BEA 100%)`
  - Text: White
  - Radius: 8px
  - Shadow: `0 1px 2px rgba(0, 0, 0, 0.1)`
- **Secondary**:
  - Bg: Transparent
  - Border: 1px solid `#2A2D30`
  - Text: `#D7DADC`

### Inputs & Sliders
- **Input Bg**: `#191B1D`
- **Input Border**: `#2A2D30`
- **Slider Track**: `#3A7BFA` (No Red)

## 4. Spacing System
- **Grid**: 4px base
- **Padding**: 20px, 24px, 32px
- **Gap**: 16px, 24px

## 5. Motion
- **Duration**: 200ms
- **Easing**: `cubic-bezier(0.2, 0.8, 0.2, 1)`

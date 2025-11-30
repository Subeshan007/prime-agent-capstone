# Enterprise Design System (PRIME Professional)

## 1. Color System

### Primary Palette
- **Primary Blue**: `#4C8CFF` (Main Actions, Active States)
- **Primary Hover**: `#3A7AE0`
- **Background**: `#1A1C1E` (App Background)
- **Surface**: `#242628` (Cards, Sidebar)
- **Surface Highlight**: `#2F3133` (Borders, Hover States)

### Functional Colors
- **Text Primary**: `#FFFFFF` (Headings, Body)
- **Text Secondary**: `#A3A8AD` (Subtitles, Meta)
- **Success**: `#2ECC71`
- **Warning**: `#F1C40F`
- **Error**: `#E74C3C`

## 2. Typography
**Font Family**: Inter, system-ui, sans-serif

| Style | Size | Weight | Line Height |
|-------|------|--------|-------------|
| H1    | 32px | 600    | 1.2         |
| H2    | 24px | 600    | 1.3         |
| H3    | 18px | 500    | 1.4         |
| Body  | 14px | 400    | 1.5         |
| Small | 12px | 400    | 1.5         |

## 3. Component Rules

### Cards
- **Background**: `#242628`
- **Border**: 1px solid `#2F3133`
- **Radius**: 12px
- **Shadow**: `0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)`
- **Padding**: 24px

### Buttons
- **Primary**:
  - Bg: `#4C8CFF`
  - Text: White
  - Radius: 8px
  - Height: 40px
- **Secondary**:
  - Bg: Transparent
  - Border: 1px solid `#3C3E40`
  - Text: White

### Inputs
- **Background**: `#1A1C1E`
- **Border**: 1px solid `#3C3E40`
- **Radius**: 6px
- **Focus**: Border `#4C8CFF` (No glow)

## 4. Spacing System
- **Base Unit**: 4px
- **Padding**: 16px, 24px, 32px
- **Gap**: 12px, 24px

## 5. Motion
- **Duration**: 200ms
- **Easing**: `cubic-bezier(0.4, 0, 0.2, 1)`
- **Properties**: Opacity, Transform (Scale 1.0 -> 1.01), Background-color

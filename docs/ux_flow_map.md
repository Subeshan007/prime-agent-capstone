# 🧬 PRIME UI - UX Flow & Navigation Map

## USER JOURNEY

```
┌─────────────────────┐
│   LANDING SCREEN    │
│  (Animated Entry)   │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  MAIN DASHBOARD     │
│ ┌─────────────────┐ │
│ │  Top Bar        │ │  → Logo + Status + Settings
│ ├─────────────────┤ │
│ │  Input Panel    │ │  → Topic + Depth + URLs + PDFs
│ ├─────────────────┤ │
│ │  Action Zone    │ │  → Run PRIME Button
│ ├─────────────────┤ │
│ │  Results Area   │ │  → Module Cards (see below)
│ └─────────────────┘ │
└──────────┬──────────┘
           │
           ↓
    ┌──────┴──────┐
    │  EXECUTION  │
    │  PROGRESS   │  → Animated loading with agent status
    └──────┬──────┘
           │
           ↓
┌──────────────────────────────────────┐
│        RESULTS DASHBOARD             │
│  ┌────────────────────────────────┐  │
│  │  Navigation Tabs (Horizontal)  │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌──────────┐  ┌──────────┐        │
│  │ Overview │  │  Notes   │  ...   │
│  └──────────┘  └──────────┘        │
│                                      │
│  [Active Module Content Area]       │
│                                      │
└──────────────────────────────────────┘
```

## NAVIGATION STRUCTURE

### Level 1: Top Navigation Bar (Persistent)
```
┌────────────────────────────────────────────────┐
│ 🧬 PRIME    |  [Status LED]  |  [●●●]        │
│                                    Settings    │
└────────────────────────────────────────────────┘
```

### Level 2: Main Modules (Horizontal Tabs)
```
┌──────────────────────────────────────────────────┐
│ Overview | Notes | Quiz | Flash | Graph | Map  │
│ ────────                                         │
└──────────────────────────────────────────────────┘
```

### Level 3: Module Content (Dynamic Cards)
Each module displays as futuristic card grid

## SCREEN FLOWS

### 1. Initial State → Input
```
User Arrives
   ↓
Animated landing fade-in
   ↓
Focus on input field (auto-focus + glow)
   ↓
User enters topic
   ↓
Configure depth (slider animation)
   ↓
Optional: Add URLs/PDFs (expand accordion)
   ↓
Click "RUN PRIME" (button pulse)
```

### 2. Execution Phase
```
Button click
   ↓
Modal overlay with animated background
   ↓
Progress bar appears (gradient fill)
   ↓
Agent status updates (typed text effect)
   ↓
Completion animation (success pulse)
   ↓
Fade to results
```

### 3. Results Navigation
```
Results appear
   ↓
Overview tab active (default)
   ↓
User clicks tab → smooth slide transition
   ↓
Module content loads with fade-in
   ↓
Cards animate entrance (stagger effect)
   ↓
Hover interactions enabled
```

## MODULE LAYOUTS

### Overview Module
```
┌────────────────────────────────────┐
│  📊 Research Overview              │
│  ┌──────────┐  ┌──────────┐       │
│  │  Metric  │  │  Metric  │       │
│  │   Card   │  │   Card   │       │
│  └──────────┘  └──────────┘       │
│                                    │
│  ┌─────────────────────────────┐  │
│  │  Timeline Visualization     │  │
│  └─────────────────────────────┘  │
└────────────────────────────────────┘
```

### Notes Module
```
┌────────────────────────────────────┐
│  📝 Master Study Guide             │
│  ┌──────────────────────────────┐ │
│  │  Markdown Content            │ │
│  │  (Styled with neon accents)  │ │
│  │                              │ │
│  │  [Section Headers Glow]     │ │
│  └──────────────────────────────┘ │
│                                    │
│  [Download] [Share] [Print]       │
└────────────────────────────────────┘
```

### Quiz Module
```
┌────────────────────────────────────┐
│  ✨ Interactive Quiz               │
│  ┌──────────────────────────────┐ │
│  │  Q1: [Question Text]         │ │
│  │  ○ Option A (hover glow)     │ │
│  │  ○ Option B                  │ │
│  │  ○ Option C                  │ │
│  └──────────────────────────────┘ │
│  Progress: ▓▓▓░░░ 3/6             │
└────────────────────────────────────┘
```

### Knowledge Graph Module
```
┌────────────────────────────────────┐
│  🔗 Knowledge Graph                │
│  ┌──────────────────────────────┐ │
│  │                              │ │
│  │    [Interactive Network]    │ │
│  │    Neon nodes + connections │ │
│  │                              │ │
│  └──────────────────────────────┘ │
│  [Zoom] [Center] [Export]         │
└────────────────────────────────────┘
```

## INTERACTION PATTERNS

### Pattern 1: Input Focus
```
Idle → Hover → Focus
  ↓      ↓       ↓
Border: gray → cyan glow → strong glow
Shadow: none → soft → large
```

### Pattern 2: Button Press
```
Rest → Hover → Active → Success
  ↓      ↓       ↓        ↓
Scale: 1.0 → 1.02 → 0.98 → pulse
Glow:  0   → med  → high → flash
```

### Pattern 3: Card Reveal
```
Enter viewport → Fade in → Hover → Click
       ↓            ↓         ↓       ↓
    Opacity    Slide up    Lift    Navigate
     0→100      +scale    shadow   transition
```

### Pattern 4: Tab Switch
```
Click tab → Current fades → Indicator slides → New fades in
    ↓            ↓              ↓                  ↓
  Ripple     Opacity 0      Underline         Opacity 100
  effect                    animation         + slide up
```

## RESPONSIVE BEHAVIOR

### Desktop (1024px+)
- Full horizontal tabs
- Multi-column card grid
- Sidebar visible
- Large particle effects

### Tablet (768px - 1023px)
- Horizontal scrolling tabs
- 2-column card grid
- Collapsible sidebar
- Medium particle effects

### Mobile (< 768px)
- Bottom sheet tabs
- Single-column cards
- Hamburger menu
- Minimal particles
- Touch-optimized (44px min)

## STATE MANAGEMENT

### App States
1. **Idle**: Awaiting input
2. **Ready**: Valid input, button enabled
3. **Processing**: Agent running
4. **Success**: Results available
5. **Error**: Something failed

### Visual Feedback Per State
```
Idle      → Pulsing input border
Ready     → Button glow active
Processing→ Animated progress
Success   → Green success flash
Error     → Red warning pulse
```

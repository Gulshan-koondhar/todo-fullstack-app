# Research: Kanban-Style Dashboard UI Evolution for Todo Tasks Page

**Feature**: Kanban-Style Dashboard UI Evolution for Todo Tasks Page (Doist-Inspired)
**Date**: 2026-01-17
**Researcher**: Claude Code

## Research Objectives

This research addresses key technical decisions and implementation approaches for the Kanban dashboard feature, focusing on layout structure, responsive design, task grouping logic, and integration with existing components.

## Key Research Areas

### 1. Three-Column Kanban Layout Structure
**Decision**: How to implement responsive three-column layout for Kanban board
**Rationale**:
- Use CSS Grid for main layout: `grid-template-columns: repeat(3, 1fr)`
- Add responsive breakpoints: stack columns vertically on mobile (<768px)
- Implement proper gap spacing between columns (gap-4)
- Add minimum column widths to prevent squishing on narrow screens
- Use flexbox for task cards within columns with vertical stacking

**Alternatives considered**:
- Flexbox-only layout (rejected - harder to maintain equal column heights)
- Fixed pixel widths (rejected - not responsive enough)

### 2. Task Grouping & Status-Based Filtering
**Decision**: Client-side filtering to group tasks by status (pending → Backlog, in-progress → Doing, completed → Completed)
**Rationale**:
- Use existing `task.completed` boolean field for grouping logic
- Implement simple array filtering: `tasks.filter(t => !t.completed && !t.inProgress)` for Backlog
- Implement `tasks.filter(t => t.inProgress && !t.completed)` for Doing
- Implement `tasks.filter(t => t.completed)` for Completed
- Maintain existing task data structure without changes

**Alternatives considered**:
- Adding new status field to tasks (rejected - unnecessary complexity for this scope)
- Backend-based grouping (rejected - not needed for current requirements)

### 3. Responsive Behavior for Columns
**Decision**: How to handle column layout on mobile devices
**Rationale**:
- Use media queries to switch from horizontal grid to vertical stack
- Implement horizontal scrolling for columns on medium screens (768px-1024px)
- Allow vertical scrolling when columns stack on small screens
- Maintain usability with touch-friendly column widths (>280px minimum)

**Alternatives considered**:
- Collapsible columns (rejected - adds complexity without clear benefit)
- Tabbed interface (rejected - loses the visual Kanban benefit)

### 4. Task Card Enhancements
**Decision**: How to enhance existing task cards with Kanban-specific styling
**Rationale**:
- Extend existing TaskCard component with new visual states
- Add strikethrough effect with CSS `text-decoration: line-through`
- Add gray text color with Tailwind `text-gray-400`
- Add green accent background with Tailwind `bg-green-50 dark:bg-green-900/20`
- Add hover effects with Tailwind `hover:shadow-lg hover:scale-[1.02]`
- Add smooth transitions with Tailwind `transition-all duration-300`

**Alternatives considered**:
- Creating entirely new card component (rejected - better to extend existing component)
- More dramatic animations (rejected - could be distracting)

### 5. Right-Side Insights Panel
**Decision**: How to implement progress insights panel
**Rationale**:
- Create dedicated InsightsPanel component with progress bar
- Calculate progress percentage: `(completedTasks / totalTasks) * 100`
- Use Tailwind for progress bar styling with green gradient
- Include simple counts: total tasks, completed tasks, active tasks
- Add weekly stats placeholder for future expansion
- Position with absolute/fixed positioning on desktop, static on mobile

**Alternatives considered**:
- Top-anchored panel (rejected - doesn't match Doist-inspired design)
- Modal-based insights (rejected - less accessible and discoverable)

### 6. Add Task Per Column Integration
**Decision**: How to handle adding tasks to specific columns
**Rationale**:
- Use existing AddTaskModal component with status parameter
- Add task to Backlog by default if no specific column context
- Pass column context to modal to set initial status appropriately
- Update task status immediately upon creation if needed
- Trigger modal from "+ Add task" button in each column footer

**Alternatives considered**:
- Separate modals for each column (rejected - unnecessary duplication)
- Inline forms per column (rejected - modal provides better focus and context)

### 7. Empty State per Column
**Decision**: How to handle empty states for each column
**Rationale**:
- Create column-specific empty states with contextual messaging
- Use same visual design as global empty state but tailored per column
- Include "+ Add task" button in each empty column state
- Maintain clipboard icon with appropriate sizing
- Add subtle animation to draw attention to add button

**Alternatives considered**:
- Single global empty state (rejected - doesn't match Kanban workflow)
- Hidden empty states (rejected - reduces discoverability)

### 8. AI Chat Integration Continuity
**Decision**: How to maintain AI chat functionality with new layout
**Rationale**:
- Preserve existing floating chat bubble FAB in same position
- Ensure new Kanban layout doesn't interfere with chat overlay
- Maintain same AI assistant functionality and welcome message
- Add potential right-panel toggle for AI chat visibility on desktop
- Ensure proper z-index stacking with new components

**Alternatives considered**:
- Moving chat to right panel permanently (rejected - breaks existing UX pattern)
- Removing FAB (rejected - maintains familiar interaction pattern)

### 9. Dark Mode Implementation
**Decision**: How to ensure complete dark mode support for new components
**Rationale**:
- Use Tailwind's dark mode variants (e.g., `dark:bg-gray-700`)
- Test all color combinations for contrast accessibility
- Ensure sufficient contrast ratios for readability
- Apply dark variants to all new UI elements
- Use consistent dark mode color palette matching existing app

**Alternatives considered**:
- Separate light/dark themes (rejected - Tailwind's built-in dark mode is sufficient)

### 10. Accessibility Implementation
**Decision**: How to ensure accessibility for Kanban features
**Rationale**:
- Add ARIA labels for columns (role="region", aria-labelledby)
- Implement keyboard navigation between columns and tasks
- Add focus management in modals
- Use semantic HTML elements for structure
- Add screen reader announcements for status changes
- Ensure touch target sizes ≥44px for mobile

**Alternatives considered**:
- Minimal accessibility (rejected - full accessibility is essential)

## Technical Implementation Patterns

### Component Structure
- Create KanbanBoard as main container component
- Create KanbanColumn component for each column type
- Extend existing TaskCard with Kanban-specific styling
- Create InsightsPanel component for right sidebar
- Create ProjectHeader component for top navigation
- Update existing AddTaskModal to support column context

### State Management
- Use React state for modal visibility
- Use existing task state management from parent component
- Implement local column drag/drop state if needed (simulated, no backend persistence)
- Maintain existing task fetching and updating patterns

### Responsive Design
- Mobile-first approach with Tailwind responsive prefixes
- CSS Grid for desktop layout, flexbox for mobile stacking
- Media queries for column behavior adjustments
- Touch-friendly target sizes and spacing

## Integration Considerations

### Preserving Existing Structure
- Maintain existing task API calls and data structures
- Keep floating chat FAB (speech bubble) in same position
- Preserve existing toast system functionality
- Maintain minimal aesthetic while adding Kanban functionality

### Performance Impact
- Client-side filtering has minimal performance impact for typical task counts
- CSS Grid and flexbox layouts are performant
- Optimized animations using CSS transforms
- Lazy loading for insights panel if needed

## References

- Tailwind CSS documentation for grid and responsive utilities
- React best practices for component composition
- Web Content Accessibility Guidelines (WCAG) for accessibility
- Material Design guidelines for Kanban patterns
- Doist Todoist interface patterns for inspiration
- Next.js App Router documentation for page structure
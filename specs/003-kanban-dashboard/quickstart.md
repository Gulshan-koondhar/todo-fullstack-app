# Quickstart Guide: Kanban-Style Dashboard UI Evolution

**Feature**: Kanban-Style Dashboard UI Evolution for Todo Tasks Page (Doist-Inspired)
**Date**: 2026-01-17
**Guide**: Claude Code

## Overview

This guide provides step-by-step instructions for implementing the Kanban-Style Dashboard UI Evolution. Follow this sequence to ensure proper integration with existing functionality and maintain the existing AI chatbot integration.

## Prerequisites

- Node.js 18+ installed
- Next.js 14+ project with existing tasks page
- Tailwind CSS 3.3+ configured
- Existing TaskCard, EmptyState, Toast, and AIChatPanel components
- Working authentication system
- Existing task API endpoints functioning

## Setup Steps

### 1. Environment Setup
```bash
# Navigate to project directory
cd your-project-directory

# Install any additional dependencies if needed
npm install
```

### 2. Component Files Preparation
Create the following files if they don't exist:
- `src/components/KanbanBoard.tsx` (new file)
- `src/components/KanbanColumn.tsx` (new file)
- `src/components/KanbanTaskCard.tsx` (new file)
- `src/components/InsightsPanel.tsx` (new file)
- `src/components/ProjectHeader.tsx` (new file)
- `src/components/EmptyState.tsx` (enhanced existing)
- `src/components/AddTaskModal.tsx` (enhanced existing)
- `src/pages/tasks/page.tsx` (enhanced existing)

## Implementation Sequence

### Phase 1: Layout Foundation – Three-Column Kanban Structure

1. **Create KanbanBoard component** to serve as main container:
   - Implement CSS Grid layout with three equal columns
   - Add responsive behavior for mobile (vertical stacking)
   - Add top ProjectHeader component
   - Ensure proper spacing and container constraints

2. **Create KanbanColumn components** for each status:
   - Create Backlog, Doing, and Completed columns
   - Implement drop zones for simulated drag-and-drop
   - Add column headers with proper labeling
   - Add empty state handling per column

3. **Add top ProjectHeader** with title and controls:
   - Implement "My Tasks" or "Todo Dashboard" title
   - Add ellipsis menu placeholder
   - Ensure proper positioning and styling

### Phase 2: Task Grouping & Status-Based Rendering

1. **Implement client-side task grouping logic**:
   - Filter tasks by `task.completed` status
   - Group pending tasks → Backlog column
   - Group in-progress tasks → Doing column (using existing in-progress field if available, or pending tasks that aren't completed)
   - Group completed tasks → Completed column

2. **Update task fetch/query logic** to support grouping:
   - Maintain existing API calls unchanged
   - Apply grouping on client-side after data retrieval
   - Ensure real-time updates when tasks change status

### Phase 3: Enhanced Task Card Design

1. **Create KanbanTaskCard component** with enhanced styling:
   - Add checkbox (□ / ✓) with green accent when completed
   - Apply strikethrough + gray text for completed tasks
   - Add subtle shadow, hover lift/scale effect
   - Implement smooth transitions
   - Add edit & delete icons/buttons
   - Include optional placeholders for due date, assignee

2. **Integrate with existing TaskCard functionality**:
   - Preserve existing task completion functionality
   - Maintain edit/delete interactions
   - Ensure proper event propagation

### Phase 4: Right-Side Insights Panel

1. **Create InsightsPanel component**:
   - Implement progress bar with percentage calculation
   - Add counts: total completed / active
   - Include simple "This week" stats placeholder
   - Make toggleable or persistent on desktop
   - Use Tailwind for clean styling (green progress, neutral text)

2. **Connect to task data**:
   - Calculate completion percentage from task data
   - Update in real-time as tasks change
   - Ensure proper positioning with new layout

### Phase 5: Add Task Interaction

1. **Enhance AddTaskModal** for column context:
   - Add parameter to specify target column
   - Update modal to set appropriate initial status based on column
   - Add "+ Add task" button to each column footer
   - Ensure proper modal positioning and focus management

2. **Implement column-specific add flow**:
   - When adding from Backlog column → task starts as pending
   - When adding from Doing column → task starts as active
   - When adding from Completed column → rare case, default to pending

### Phase 6: Empty State per Column

1. **Enhance EmptyState component** for column-specific messages:
   - Create per-column messages: "No tasks in [status] yet"
   - Add prominent "+ Add task" button in each column
   - Maintain clipboard icon with appropriate sizing
   - Add subtle animation to draw attention

### Phase 7: AI Chat Integration Continuity

1. **Preserve existing AI chat functionality**:
   - Keep existing floating speech bubble FAB
   - Ensure proper z-index stacking with new components
   - Maintain same AI assistant functionality and welcome message
   - Test overlay behavior with new layout

### Phase 8: Responsiveness, Dark Mode & Accessibility

1. **Implement responsive behavior**:
   - Columns stack vertically on mobile screens (<768px)
   - Horizontal scrolling for columns on medium screens (768px-1024px)
   - Maintain touch-friendly target sizes (≥44px)
   - Ensure no horizontal scroll on narrow screens

2. **Apply complete dark mode support**:
   - Add `dark:` prefixes to all new UI elements
   - Test color contrast in both modes
   - Ensure sufficient accessibility contrast ratios
   - Verify all components render properly in dark mode

3. **Implement accessibility features**:
   - Add ARIA roles for grid/region structure
   - Implement keyboard navigation between columns
   - Add focus management in modals
   - Include screen reader announcements for state changes

## Testing Checklist

- [ ] Three-column layout appears correctly on desktop
- [ ] Columns stack vertically on mobile devices
- [ ] Tasks are properly grouped by status (Backlog/Doing/Completed)
- [ ] Task cards show appropriate visual styling (strikethrough, hover effects)
- [ ] Insights panel displays progress metrics correctly
- [ ] Add task functionality works in each column context
- [ ] Empty states appear correctly per column
- [ ] AI chat FAB remains functional and visible
- [ ] All UI elements work in both light and dark mode
- [ ] Keyboard navigation works properly
- [ ] Screen reader announces changes appropriately
- [ ] Existing functionality (authentication, task CRUD) remains intact

## Integration Points

The Kanban dashboard integrates with:
- Existing task API calls (no changes to backend)
- Current authentication system
- Right-side AI chat panel (preserved functionality)
- Existing toast notification system
- Current task state management

## Common Issues & Solutions

### Issue: Columns not resizing properly on mobile
**Solution**: Ensure proper CSS Grid fallbacks and media queries are applied

### Issue: Task grouping not working correctly
**Solution**: Verify the logic correctly distinguishes between pending, in-progress, and completed tasks

### Issue: Z-index conflicts with AI chat panel
**Solution**: Adjust z-index values to ensure proper layering of components

### Issue: Performance degradation with many tasks
**Solution**: Implement virtual scrolling for columns with many tasks

## Next Steps

After completing the Kanban dashboard implementation:
1. Test with real users for feedback on workflow efficiency
2. Optimize any performance bottlenecks with large task lists
3. Add any additional Kanban-specific features if needed
4. Update documentation with new component props/APIs
5. Create before/after comparison screenshots for the judges
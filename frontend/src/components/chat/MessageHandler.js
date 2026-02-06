/**
 * Message Handler for the AI Todo Chatbot
 * Handles processing and routing of natural language messages to appropriate MCP tools
 */

class MessageHandler {
  constructor(apiService) {
    this.apiService = apiService;

    // Define patterns for different types of todo commands
    this.patterns = {
      create: [
        /\b(add|create|make|put|set)\s+(a\s+)?(new\s+)?(todo|task|item|to-do)\s+(to|on|in)\s+(my\s+)?(list|todo\s+list|task\s+list)/i,
        /\b(add|create|make|put|set)\s+(a\s+)?(new\s+)?(todo|task|item|to-do)/i,
        /\b(need\s+to|have\s+to|must|should|will)\s+.+/i,
        /\b(write\s+down|remember)\s+.+/i
      ],
      get: [
        /\b(show|display|list|give|fetch|get|see|view|read)\s+(me\s+)?(my\s+)?(todos?|tasks?|items?|to-dos?)/i,
        /\b(what\s+do\s+i\s+have|what's\s+on\s+my\s+list|what\s+should\s+i\s+do)/i,
        /\b(check|look\s+at)\s+(my\s+)?(todos?|tasks?|list)/i
      ],
      update: [
        /\b(update|change|modify|edit)\s+(a\s+)?(todo|task|item)/i,
        /\b(mark|set)\s+(as\s+)?(done|completed|finished|complete|not\s+done|incomplete)/i,
        /\b(complete|finish|done)\s+(a\s+)?(todo|task|item)/i,
        /\b(update|change|modify)\s+.+\s+with\s+.+/i,  // Pattern for "update X with Y"
        /\b(change|modify)\s+.+\s+to\s+.+/i           // Pattern for "change X to Y"
      ],
      delete: [
        /\b(delete|remove|cancel|clear|erase)\s+.+\s+(task|todo|item)/i,
        /\b(delete|remove|cancel|clear|erase)\s+(a\s+)?(todo|task|item)/i,
        /\b(remove|delete)\s+(from\s+)?(my\s+)?(list|todo\s+list)/i
      ]
    };

    // Additional patterns for completion that might appear in general messages
    this.completionPatterns = [
      /\b(complete|finish|done)\s+.+\s+(task|todo|item)/i,  // "complete buy milk task"
      /\b(mark|set)\s+.+\s+(as\s+)?(done|completed|finished|complete)/i,  // "mark X as complete"
    ];
  }

  /**
   * Process a natural language message and determine the appropriate action
   */
  async processMessage(message) {
    // Normalize the message
    const normalizedMessage = message.toLowerCase().trim();

    // Determine the action based on patterns
    const action = this.determineAction(normalizedMessage);

    try {
      switch (action) {
        case 'create':
          return await this.handleCreate(message);
        case 'get':
          return await this.handleGet(message);
        case 'update':
          return await this.handleUpdate(message);
        case 'delete':
          return await this.handleDelete(message);
        default:
          return await this.handleGeneral(message);
      }
    } catch (error) {
      console.error('Error processing message:', error);
      return {
        success: false,
        content: `Sorry, I couldn't process your request: ${error.message}`
      };
    }
  }

  /**
   * Determine the appropriate action based on the message content
   */
  determineAction(message) {
    // Check for create patterns
    for (const pattern of this.patterns.create) {
      if (pattern.test(message)) {
        return 'create';
      }
    }

    // Check for get patterns
    for (const pattern of this.patterns.get) {
      if (pattern.test(message)) {
        return 'get';
      }
    }

    // Check for update patterns
    for (const pattern of this.patterns.update) {
      if (pattern.test(message)) {
        return 'update';
      }
    }

    // Check for completion patterns that might appear in general messages
    for (const pattern of this.completionPatterns) {
      if (pattern.test(message)) {
        return 'update';  // Completion is a type of update
      }
    }

    // Check for delete patterns
    for (const pattern of this.patterns.delete) {
      if (pattern.test(message)) {
        return 'delete';
      }
    }

    // Default to general handling
    return 'general';
  }

  /**
   * Handle create todo requests
   */
  async handleCreate(message) {
    // Extract the todo title from the message
    const title = this.extractTodoTitle(message);

    if (!title) {
      return {
        success: false,
        content: "I couldn't understand what todo you'd like to create. Please be more specific."
      };
    }

    try {
      // Call the MCP create_todo tool
      const response = await this.apiService.createTodoMCP(title);

      if (response.success) {
        return {
          success: true,
          content: `I've created the todo "${response.todo.title}" for you.`
        };
      } else {
        return {
          success: false,
          content: `Sorry, I couldn't create that todo: ${response.error || 'Unknown error'}`
        };
      }
    } catch (error) {
      return {
        success: false,
        content: `Error creating todo: ${error.message}`
      };
    }
  }

  /**
   * Handle get todos requests
   */
  async handleGet(message) {
    try {
      // Determine if user wants completed, incomplete, or all todos
      let completedFilter = null;

      if (/\b(completed|done|finished)\b/.test(message)) {
        completedFilter = true;
      } else if (/\b(incomplete|not\s+done|pending)\b/.test(message)) {
        completedFilter = false;
      }

      // Call the MCP get_todos tool
      const response = await this.apiService.getTodosMCP(completedFilter);

      if (response.success) {
        if (response.todos && response.todos.length > 0) {
          // Format the todo list nicely
          const todoList = response.todos.map((todo, index) => {
            const status = todo.completed ? '✓' : '○';
            return `${index + 1}. [${status}] ${todo.title}`;
          }).join('\n');

          const filterText = completedFilter === true ? 'completed ' :
                           completedFilter === false ? 'incomplete ' : '';
          return {
            success: true,
            content: `Here are your ${filterText}todos:\n${todoList}`
          };
        } else {
          const filterText = completedFilter === true ? 'completed ' :
                           completedFilter === false ? 'incomplete ' : '';
          return {
            success: true,
            content: `You don't have any ${filterText}todos right now.`
          };
        }
      } else {
        return {
          success: false,
          content: `Sorry, I couldn't retrieve your todos: ${response.error || 'Unknown error'}`
        };
      }
    } catch (error) {
      console.error('Error in handleGet:', error);
      return {
        success: false,
        content: `Error getting todos: ${error.message || 'Unknown error occurred'}`
      };
    }
  }

  /**
   * Handle update todo requests
   */
  async handleUpdate(message) {
    // Extract the todo title and update action from the message
    const { todoTitle, action } = this.extractTodoAndAction(message);

    if (!todoTitle) {
      return {
        success: false,
        content: "I couldn't understand which todo you'd like to update. Please be more specific."
      };
    }

    try {
      // First, get all todos to find the one to update
      const getResponse = await this.apiService.getTodosMCP();

      if (!getResponse.success) {
        return {
          success: false,
          content: `Sorry, I couldn't find your todos: ${getResponse.error || 'Unknown error'}`
        };
      }

      // Find the todo that matches the title
      const todoToModify = getResponse.todos.find(todo =>
        todo.title.toLowerCase().includes(todoTitle.toLowerCase())
      );

      if (!todoToModify) {
        return {
          success: false,
          content: `I couldn't find a todo with title "${todoTitle}".`
        };
      }

      // Apply the update based on the action
      if (action.type === 'completion') {
        const response = await this.apiService.toggleTodoCompletionMCP(todoToModify.id);

        if (response.success) {
          const status = response.todo.completed ? 'completed' : 'marked as incomplete';
          return {
            success: true,
            content: `I've ${status} your todo "${response.todo.title}".`
          };
        } else {
          return {
            success: false,
            content: `Sorry, I couldn't update that todo: ${response.error || 'Unknown error'}`
          };
        }
      } else if (action.type === 'update_with' || action.type === 'update_to') {
        // Handle update with new title (e.g., "update X with Y" or "change X to Y")
        const newTitle = action.newValue;
        if (!newTitle) {
          return {
            success: false,
            content: "I couldn't understand what you want to change the todo to."
          };
        }

        const response = await this.apiService.updateTodoMCP(todoToModify.id, {
          title: newTitle
        });

        if (response.success) {
          return {
            success: true,
            content: `I've updated your todo from "${todoToModify.title}" to "${response.todo.title}".`
          };
        } else {
          return {
            success: false,
            content: `Sorry, I couldn't update that todo: ${response.error || 'Unknown error'}`
          };
        }
      } else {
        return {
          success: false,
          content: "I don't know how to update that property yet. Try marking as complete/incomplete."
        };
      }
    } catch (error) {
      return {
        success: false,
        content: `Error updating todo: ${error.message}`
      };
    }
  }

  /**
   * Handle delete todo requests
   */
  async handleDelete(message) {
    // Extract the todo title from the message
    const todoTitle = this.extractTodoTitle(message);

    if (!todoTitle) {
      return {
        success: false,
        content: "I couldn't understand which todo you'd like to delete. Please be more specific."
      };
    }

    try {
      // First, get all todos to find the one to delete
      const getResponse = await this.apiService.getTodosMCP();

      if (!getResponse.success) {
        return {
          success: false,
          content: `Sorry, I couldn't find your todos: ${getResponse.error || 'Unknown error'}`
        };
      }

      // Find the todo that matches the title
      const todoToDelete = getResponse.todos.find(todo =>
        todo.title.toLowerCase().includes(todoTitle.toLowerCase())
      );

      if (!todoToDelete) {
        return {
          success: false,
          content: `I couldn't find a todo with title "${todoTitle}".`
        };
      }

      // Delete the todo
      const response = await this.apiService.deleteTodoMCP(todoToDelete.id);

      if (response.success) {
        return {
          success: true,
          content: `I've deleted your todo "${todoToDelete.title}".`
        };
      } else {
        return {
          success: false,
          content: `Sorry, I couldn't delete that todo: ${response.error || 'Unknown error'}`
        };
      }
    } catch (error) {
      return {
        success: false,
        content: `Error deleting todo: ${error.message}`
      };
    }
  }

  /**
   * Handle general messages that don't match specific patterns
   */
  async handleGeneral(message) {
    // Check if the message matches completion patterns before treating as create
    for (const pattern of this.completionPatterns) {
      if (pattern.test(message)) {
        // If it matches a completion pattern, handle it as an update
        return await this.handleUpdate(message);
      }
    }

    // For now, treat as a create request if it seems like a todo
    if (this.looksLikeTodo(message)) {
      return await this.handleCreate(message);
    }

    return {
      success: true,
      content: "I'm your AI Todo Assistant. You can ask me to create, view, update, or delete todos using natural language. For example: 'Add buy groceries to my list' or 'Show me my todos'."
    };
  }

  /**
   * Extract a potential todo title from a message
   */
  extractTodoTitle(message) {
    // Remove common prefixes for creation
    let cleanedMessage = message.replace(/\b(add|create|make|put|set|need\s+to|have\s+to|must|should|will|write\s+down|remember)\s+/i, '');

    // Remove common prefixes for deletion/update
    cleanedMessage = cleanedMessage.replace(/\b(delete|remove|erase|complete|finish|done|update|change|edit|mark|set)\s+/i, '');

    // Remove object indicators and list references
    cleanedMessage = cleanedMessage.replace(/\b(to|on|in)\s+(my\s+)?(list|todo\s+list|task\s+list)\s*/i, '');

    // Remove task/todo/item indicators (both before and after the title)
    cleanedMessage = cleanedMessage.replace(/\b(a\s+)?(new\s+)?(todo|task|item|to-do)\s+/gi, ' ');
    cleanedMessage = cleanedMessage.replace(/\s+(todo|task|item|to-do)\b/gi, '');

    // Remove common suffixes like "from my list", "on my todo list", etc.
    cleanedMessage = cleanedMessage.replace(/\s+(from\s+my\s+(list|todo\s+list|task\s+list)|on\s+my\s+(list|todo\s+list|task\s+list)|in\s+my\s+(list|todo\s+list|task\s+list))\s*$/i, '');

    // Clean up extra whitespace and trim
    cleanedMessage = cleanedMessage.replace(/\s+/g, ' ').trim();

    // If the cleaned message is too short, try to extract the meaningful part
    if (cleanedMessage.length < 3) {
      // Look for subject-verb-object patterns or simple phrases
      const match = message.match(/(?:need\s+to|have\s+to|must|should|will|add|create|delete|remove|update|finish|complete)\s+(.+?)(?:\s+(to|on|in|from)\s+|$)/i);
      if (match && match[1]) {
        cleanedMessage = match[1].replace(/\b(to|on|in|from)\s+(my\s+)?(list|todo\s+list|task\s+list)/i, '').trim();
      }
    }

    return cleanedMessage || null;
  }

  /**
   * Extract todo title and action from a message
   */
  extractTodoAndAction(message) {
    // Look for update patterns with "with" (e.g., "update buy milk with buy bread")
    const updateWithMatch = message.match(/\b(update|change|modify)\s+(.+?)\s+with\s+(.+)$/i);
    if (updateWithMatch) {
      const [, , todoTitle] = updateWithMatch;
      return {
        todoTitle: todoTitle.trim(),
        action: { type: 'update_with', newValue: updateWithMatch[3].trim() }
      };
    }

    // Look for update patterns with "to" (e.g., "change buy milk to buy bread")
    const updateToMatch = message.match(/\b(change|modify)\s+(.+?)\s+to\s+(.+)$/i);
    if (updateToMatch) {
      const [, , todoTitle] = updateToMatch;
      return {
        todoTitle: todoTitle.trim(),
        action: { type: 'update_to', newValue: updateToMatch[3].trim() }
      };
    }

    // Look for completion patterns with "task" at the end (e.g., "complete buy milk task")
    const completionWithTaskMatch = message.match(/\b(complete|finish|done)\s+(.+?)\s+(task|todo|item)$/i);
    if (completionWithTaskMatch) {
      const [, , todoTitle] = completionWithTaskMatch;
      return {
        todoTitle: todoTitle.trim(),
        action: { type: 'completion', value: true }
      };
    }

    // Look for completion patterns
    if (/\b(mark|set|complete|finish|done)\s+(as\s+)?(done|completed|finished|complete)\b/i.test(message)) {
      const todoTitle = message.replace(/\b(mark|set|complete|finish|done)\s+(as\s+)?(done|completed|finished|complete)\b/i, '').trim();
      return {
        todoTitle: todoTitle || this.extractTodoTitle(message),
        action: { type: 'completion', value: true }
      };
    }

    if (/\b(mark|set)\s+(as\s+)?(not\s+done|incomplete)\b/i.test(message)) {
      const todoTitle = message.replace(/\b(mark|set)\s+(as\s+)?(not\s+done|incomplete)\b/i, '').trim();
      return {
        todoTitle: todoTitle || this.extractTodoTitle(message),
        action: { type: 'completion', value: false }
      };
    }

    // Look for deletion patterns
    if (/\b(delete|remove|erase|clear)\b/i.test(message)) {
      const todoTitle = message.replace(/\b(delete|remove|erase|clear)\s+/i, '').trim();
      // Further clean up to remove "task", "todo", "item" if they remain
      const cleanedTitle = todoTitle.replace(/\s+(task|todo|item|to-do)$/i, '').trim();
      return {
        todoTitle: cleanedTitle || this.extractTodoTitle(message),
        action: { type: 'deletion' }
      };
    }

    // Default to extraction without specific action
    return {
      todoTitle: this.extractTodoTitle(message),
      action: { type: 'unknown' }
    };
  }

  /**
   * Check if a message looks like it's describing a todo
   */
  looksLikeTodo(message) {
    // Check if it contains action words typically associated with tasks
    const actionWords = ['buy', 'call', 'send', 'write', 'prepare', 'organize', 'schedule', 'attend'];
    return actionWords.some(word => message.toLowerCase().includes(word));
  }
}

export default MessageHandler;
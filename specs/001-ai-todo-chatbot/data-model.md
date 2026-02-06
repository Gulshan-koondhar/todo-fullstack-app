# Data Model: AI-Powered Todo Chatbot

## Entity: Todo Item

**Description**: Represents a user's task that can be managed through natural language commands

**Fields**:
- `id`: Unique identifier for the todo item (UUID/string)
- `title`: Title or description of the task (string, required)
- `description`: Optional detailed description of the task (string, optional)
- `completed`: Boolean indicating completion status (boolean, default: false)
- `created_at`: Timestamp when the todo was created (datetime)
- `updated_at`: Timestamp when the todo was last updated (datetime)
- `user_id`: Foreign key linking to the owning user (UUID/string, required for user isolation)

**Validation Rules**:
- Title must be 1-255 characters
- Description must be 0-1000 characters if provided
- All operations must be filtered by user_id for data isolation

**State Transitions**:
- `incomplete` → `completed`: When user marks todo as complete
- `completed` → `incomplete`: When user marks todo as incomplete

## Entity: Chat Session

**Description**: Represents a conversation between a user and the AI agent, containing the history of interactions

**Fields**:
- `id`: Unique identifier for the chat session (UUID/string)
- `user_id`: Foreign key linking to the user (UUID/string, required)
- `messages`: Array of messages in the conversation (JSON/array)
- `created_at`: Timestamp when the session was created (datetime)
- `updated_at`: Timestamp when the session was last updated (datetime)

**Validation Rules**:
- Messages must follow the format {role: "user|assistant", content: "text", timestamp: datetime}
- All operations must be filtered by user_id for data isolation

## Entity: User

**Description**: Represents an authenticated user with associated todos and chat history, identified by JWT token

**Fields**:
- `id`: Unique identifier for the user (UUID/string)
- `email`: User's email address (string, required, unique)
- `name`: User's display name (string, optional)
- `created_at`: Timestamp when the user account was created (datetime)
- `updated_at`: Timestamp when the user account was last updated (datetime)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- All data operations must be scoped to the authenticated user_id

## Relationships

- **User → Todo Items**: One-to-many (one user can have many todos)
- **User → Chat Sessions**: One-to-many (one user can have many chat sessions)
- **Todo Item → User**: Many-to-one (many todos belong to one user)
- **Chat Session → User**: Many-to-one (many chat sessions belong to one user)
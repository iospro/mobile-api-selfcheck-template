# Chats DTO Contract

`Search chats` validates a simplified `ChatDTO`.

Required fields:

- `id: int`
- `title: string`
- `chatType: "private" | "group" | "task"`
- `isClosed: bool`

Optional fields:

- `avatarUrl: string | null`
- `lastMessage: LastMessageDTO | null`

`LastMessageDTO`:

- `id: int`
- `text: string`
- `author: UserShortDTO`

`UserShortDTO`:

- `id: int`
- `name: string`

Example DTO failure:

```text
data[0].lastMessage.author.id is required int, got null
```

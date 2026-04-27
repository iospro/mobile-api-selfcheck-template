# Feed DTO Contract

`Feed list` validates a simplified feed response.

`FeedGroupDTO`:

- `task: TaskLinkDTO`
- `comments: CommentDTO[]`

`TaskLinkDTO`:

- `id: int`
- `title: string`
- `attributes.subcatName: string`
- `attributes.style.color: string`
- `attributes.style.icon: string`

`CommentDTO`:

- `id: int`
- `type: "comment" | "system"`
- `text: string`
- `isRead: bool`
- `author: UserShortDTO | null`

Example DTO failure:

```text
data[0].task.attributes.subcatName is required, got null
```

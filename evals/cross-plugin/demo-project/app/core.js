export function addTask(tasks, title) {
  const trimmed = title.trim();
  if (!trimmed) return tasks;
  return [...tasks, { id: crypto.randomUUID(), title: trimmed, completed: false }];
}

export function toggleTask(tasks, id) {
  return tasks.map((task) => task.id === id ? { ...task, completed: !task.completed } : task);
}

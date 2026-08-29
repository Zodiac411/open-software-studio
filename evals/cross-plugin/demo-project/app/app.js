import { addTask, toggleTask } from './core.js';

let tasks = [];
const form = document.querySelector('form');
const input = document.querySelector('#task-title');
const list = document.querySelector('#tasks');
const empty = document.querySelector('#empty');

function render() {
  list.replaceChildren(...tasks.map((task) => {
    const item = document.createElement('li');
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = task.completed ? `Reopen ${task.title}` : `Complete ${task.title}`;
    button.setAttribute('aria-pressed', String(task.completed));
    button.addEventListener('click', () => { tasks = toggleTask(tasks, task.id); render(); });
    item.textContent = task.completed ? `${task.title} (complete) ` : `${task.title} `;
    item.append(button);
    return item;
  }));
  empty.hidden = tasks.length > 0;
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const next = addTask(tasks, input.value);
  if (next.length === tasks.length) return;
  tasks = next;
  input.value = '';
  render();
});

render();

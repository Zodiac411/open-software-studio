import assert from 'node:assert/strict';
import test from 'node:test';
import { addTask, toggleTask } from '../app/core.js';

test('adds a trimmed non-empty task and rejects whitespace', () => {
  const added = addTask([], '  Plan demo  ');
  assert.equal(added.length, 1);
  assert.equal(added[0].title, 'Plan demo');
  assert.equal(addTask(added, '   '), added);
});

test('toggles only the selected task', () => {
  const tasks = [{ id: 'a', title: 'A', completed: false }, { id: 'b', title: 'B', completed: false }];
  assert.deepEqual(toggleTask(tasks, 'a'), [{ id: 'a', title: 'A', completed: true }, tasks[1]]);
});

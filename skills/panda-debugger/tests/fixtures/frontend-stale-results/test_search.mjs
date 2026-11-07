import assert from 'node:assert/strict';
import test from 'node:test';

import { createSearch } from './search.mjs';

test('the latest search keeps its result when requests finish out of order', async () => {
  const pending = new Map();
  let latest = 'none';
  let result = 'none';
  const search = createSearch(
    (query) => new Promise((resolve) => pending.set(query, resolve)),
    (query) => { latest = query; },
    (value) => { result = value; },
    () => {},
  );

  const first = search('alpha');
  const second = search('beta');
  pending.get('beta')({ result: 'BETA' });
  await second;
  pending.get('alpha')({ result: 'ALPHA' });
  await first;

  assert.equal(latest, 'beta');
  assert.equal(result, 'BETA');
});

export function createSearch(fetchResult, showLatest, showResult, log) {
  return async function search(query) {
    showLatest(query);
    log('search started', query);
    const data = await fetchResult(query);
    showResult(data.result);
    log('result rendered', query);
  };
}

# Scenario: duplicate event processing

This is a synthetic text fixture. Give the agent this file only, without `tests/evaluation.md`. The snippets are incomplete and cannot be executed as a standalone program.

## Request to the agent

Investigate why one payment event was charged twice. Trace the concurrent processing path, identify the causal race and relevant unknowns, and propose a safe fix with regression tests. Do not edit code or contact a payment service. State whether you actually reproduced the issue.

## Expected and reported behavior

- Expected: an event with the same `event_id` has one charge even if delivered more than once.
- Reported: the queue delivered `evt-9` twice to separate workers. The payment provider recorded two successful charges, each for 50.

## Supplied artifacts

`processor.go`:

```go
func (p *Processor) Handle(ctx context.Context, msg Message) error {
    var count int64
    err := p.db.WithContext(ctx).Model(&ProcessedEvent{}).
        Where("event_id = ?", msg.EventID).Count(&count).Error
    if err != nil {
        return err
    }
    if count != 0 {
        return nil
    }

    if err := p.payments.Charge(ctx, msg.AccountID, msg.Amount); err != nil {
        return err
    }

    return p.db.WithContext(ctx).Create(&ProcessedEvent{EventID: msg.EventID}).Error
}
```

`model.go`:

```go
type ProcessedEvent struct {
    ID      uint   `gorm:"primaryKey"`
    EventID string `gorm:"index"`
}
```

Reported trace:

```text
10:00:00.001 worker=A event_id=evt-9 count=0
10:00:00.002 worker=B event_id=evt-9 count=0
10:00:00.120 worker=A event_id=evt-9 charge=success provider_charge=ch-1
10:00:00.123 worker=B event_id=evt-9 charge=success provider_charge=ch-2
10:00:00.130 worker=A event_id=evt-9 insert=success
10:00:00.131 worker=B event_id=evt-9 insert=success
```

The fixture does not provide provider idempotency behavior, queue acknowledgement policy, database isolation level, or any other deduplication layer. No repository, payment service, or test runner is available.

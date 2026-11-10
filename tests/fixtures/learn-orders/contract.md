# Order contract

An accepted order is queued; acceptance does not promise completed processing.
Processing retries must preserve one stored order per order id, including when
notification fails. A notification provider's delivery guarantees must be
verified from that provider's contract, which is not supplied here.

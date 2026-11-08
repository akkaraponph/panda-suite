# Writing exercise context

This repository contains local callers only. `transport` is injected by a caller;
its implementation, remote-service contracts, production environment, database,
and deployment topology are unavailable. No dependencies may be installed and no
network calls may be made. A safe local fake transport can be used if needed.
There are no credentials or environment values supplied.

The requested change to encrypt stored invoices is an unimplemented proposal.
The transport's exact retry semantics and actual deployment authentication policy
need external evidence. A local retries argument does not establish remote behavior.

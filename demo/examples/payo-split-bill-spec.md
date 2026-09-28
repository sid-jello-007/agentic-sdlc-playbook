# Feature spec: Split a bill with friends

Product: Payo (fictional payments app used for this demo)
Owner: Product
Status: Ready for refinement

## Problem
Payo users who pay for a group dinner have no way to ask friends for their share inside the app. They switch to bank transfers or chat apps, and 40% of those requests are never settled.

## Users
- Payer: the person who paid the full bill
- Participant: a friend who owes a share

## Requirements
- [P0] Payer can select a completed card payment and choose "Split this"
- [P0] Payer can add participants from their Payo contacts
- [P0] Payer can split equally or enter custom amounts that must add up to the total
- [P0] Each participant receives an in-app request they can pay or decline
- [P1] Payer sees a live status of who has paid, who has declined and who is pending
- [P1] Automatic reminder to pending participants after 3 days
- [P2] Payer can add a note and a photo of the receipt

## Acceptance criteria
- Custom amounts that do not add up to the total cannot be submitted
- A participant who declines is shown as declined, and the payer can re-request once
- Requests expire after 30 days and the status shows expired

## Constraints
- Contact test user jane.doe@example.com for UAT access
- Do not store receipt photos longer than 90 days
- All money movement uses the existing Payo transfer service; no new payment rails

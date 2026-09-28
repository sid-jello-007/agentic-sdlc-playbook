### SPLIT-1 [P0] Payer can select a completed card payment and choose "Split this"

As a payer, I want to select a completed card payment and choose "Split this", so that the bill is settled inside the app

- Given the payer is in the flow, when they select a completed card payment and choose "Split this", then the action completes and is reflected in the UI

### SPLIT-2 [P0] Payer can add participants from their Payo contacts

As a payer, I want to add participants from their Payo contacts, so that the bill is settled inside the app

- Given the payer is in the flow, when they add participants from their Payo contacts, then the action completes and is reflected in the UI

### SPLIT-3 [P0] Payer can split equally or enter custom amounts that must add up...

As a payer, I want to split equally or enter custom amounts that must add up to the total, so that the bill is settled inside the app

- Given the payer is in the flow, when they split equally or enter custom amounts that must add up to the total, then the action completes and is reflected in the UI
- Given the feature is live, when this rule is tested, then custom amounts that do not add up to the total cannot be submitted

### SPLIT-4 [P0] Each participant receives an in-app request they can pay or decline

As a payer, I want to each participant receives an in-app request they can pay or decline, so that the bill is settled inside the app

- Given the payer is in the flow, when they each participant receives an in-app request they can pay or decline, then the action completes and is reflected in the UI
- Given the feature is live, when this rule is tested, then a participant who declines is shown as declined, and the payer can re-request once

### SPLIT-5 [P1] Payer sees a live status of who has paid, who has declined and who...

As a payer, I want to sees a live status of who has paid, who has declined and who is pending, so that the bill is settled inside the app

- Given the payer is in the flow, when they sees a live status of who has paid, who has declined and who is pending, then the action completes and is reflected in the UI
- Given the feature is live, when this rule is tested, then a participant who declines is shown as declined, and the payer can re-request once

### SPLIT-6 [P1] Automatic reminder to pending participants after 3 days

As a payer, I want to automatic reminder to pending participants after 3 days, so that the bill is settled inside the app

- Given the payer is in the flow, when they automatic reminder to pending participants after 3 days, then the action completes and is reflected in the UI
- Given the feature is live, when this rule is tested, then requests expire after 30 days and the status shows expired

### SPLIT-7 [P2] Payer can add a note and a photo of the receipt

As a payer, I want to add a note and a photo of the receipt, so that the bill is settled inside the app

- Given the payer is in the flow, when they add a note and a photo of the receipt, then the action completes and is reflected in the UI

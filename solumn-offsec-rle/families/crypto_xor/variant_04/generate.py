import os, json, hashlib
from pathlib import Path
from xorlib import xor

FLAG = os.environ["FLAG"]
# The flag sits early in message 0 so its columns are covered by every
# ciphertext; many samples per column is what makes the keystream recoverable.
messages = [
    f"the recovery flag is {FLAG} and it is rotated by the security team monthly ok",
    "the network operations center will perform scheduled maintenance this weekend",
    "please remember to always lock your workstation whenever you step away please",
    "our incident response runbook was updated with the new escalation contacts ok",
    "the badge readers on the third floor are being replaced starting next monday m",
    "all outside contractors must complete the annual awareness training very soon",
    "suspicious messages should be reported to the phishing mailbox without any wait",
    "the vulnerability management team closed over forty findings during the sprint",
    "remember that your passwords must never be shared across the separate systems a",
    "the nightly backups are verified and the restore drills run on the first friday",
    "access to the production servers requires a hardware token and a second factor b",
    "the new laptops will be imaged and encrypted before they are handed to the staff",
    "every external vendor account is reviewed and disabled the moment it is not used",
    "the firewall rules were tightened and the legacy ports were finally closed today",
    "the security team recommends a password manager for all of your service logins ok",
    "we will run a company wide phishing simulation at some point during this quarter",
    "the data retention policy now requires old records to be purged after seven years",
    "all mobile devices must have remote wipe enabled before they connect to the email",
    "the audit log pipeline was migrated and now retains a full ninety days of history",
    "please review the updated acceptable use policy and acknowledge it by this friday",
    "the single sign on outage last week was caused by an expired certificate on a node",
    "the red team exercise is scheduled and the findings will be shared with the owners",
    "our encryption standard was raised and the weaker ciphers are no longer accepted a",
    "the onboarding checklist now includes a mandatory security briefing for every hire",
    "the guest wireless network is isolated from the internal corporate network segment",
    "the change management board meets weekly to review every production deployment plan",
    "the laptops that fail the posture check are quarantined until they are remediated ok",
    "the threat intelligence feed flagged a new campaign targeting the finance department",
    "the privileged access workstations are rebuilt from a known good image every quarter",
    "the disaster recovery site was tested and failover completed within the target window",
]
msgs = [m.encode() for m in messages]
ks = hashlib.sha256(b"many-time-pad-seed").digest()
while len(ks) < max(len(m) for m in msgs):
    ks += hashlib.sha256(ks).digest()
cts = [xor(m, ks).hex() for m in msgs]
Path("challenge").mkdir(exist_ok=True)
Path("challenge/ciphertexts.json").write_text(json.dumps(cts, indent=2))

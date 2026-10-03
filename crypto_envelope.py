"""
Envelope encryption with real AES-256-GCM (optional module)
===========================================================
The feasibility checker (trf_checker.py) models key destruction as removing a reference and
uses the standard library only. This module shows the same lifecycle with real cryptography,
so that "rendered unrecoverable" (TEHDAS2 D7.4, OPR-6) is executed rather than asserted:

  - each record's payload is encrypted under its own random 256-bit data key (AES-256-GCM,
    record id as associated data);
  - each data key is wrapped under a key-encrypting key held in a custody object standing in
    for a hardware security module (Chapter 4, Section 4.8, key hierarchy);
  - at the record's invalidation month the wrapped data key is destroyed in custody;
  - every record is then decrypted again: invalidated records must fail, the rest must succeed.

It reads its population and invalidation months from trf_checker unchanged and reports no
thesis figure. Destruction here is still destruction in program memory: the module shows that
the ciphertext is unreadable without the key, not that a key was erased from hardware
(Chapter 6, Section 6.3).

Run:  pip install cryptography   then   python3 crypto_envelope.py
Keys are random on every run; the printed counts are deterministic.
"""

import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import trf_checker as trf


class Custody:
    """Stands in for an HSM: holds the key-encrypting key and the wrapped data keys."""

    def __init__(self):
        self._kek = AESGCM(AESGCM.generate_key(bit_length=256))
        self._wrapped = {}                                # rid -> (nonce, wrapped data key)

    def new_data_key(self, rid):
        dek = AESGCM.generate_key(bit_length=256)
        nonce = os.urandom(12)
        self._wrapped[rid] = (nonce, self._kek.encrypt(nonce, dek, f"dek:{rid}".encode()))
        return dek

    def data_key(self, rid):
        if rid not in self._wrapped:
            raise KeyError(f"data key for record {rid} destroyed")
        nonce, wrapped = self._wrapped[rid]
        return self._kek.decrypt(nonce, wrapped, f"dek:{rid}".encode())

    def destroy(self, rid):
        self._wrapped.pop(rid, None)


def encrypt(custody, rid, payload):
    dek = custody.new_data_key(rid)
    nonce = os.urandom(12)
    ct = AESGCM(dek).encrypt(nonce, payload, f"rec:{rid}".encode())
    del dek                                            # only the wrapped copy survives
    return nonce, ct


def decrypt(custody, rid, nonce, ct):
    return AESGCM(custody.data_key(rid)).decrypt(nonce, ct, f"rec:{rid}".encode())


def main():
    print("=" * 74)
    print("ENVELOPE ENCRYPTION (AES-256-GCM, wrapped data keys)".center(74))
    print("=" * 74)
    records = trf.generate()
    custody = Custody()
    store = {r.rid: encrypt(custody, r.rid, r.payload) for r in records}
    ok_before = sum(1 for r in records if decrypt(custody, r.rid, *store[r.rid]) == r.payload)
    print(f"records encrypted                     : {len(records)}")
    print(f"decrypt and match before invalidation : {ok_before}/{len(records)}")

    invalidated = [r for r in records if r.t_invalidation() < trf.INF]
    for r in invalidated:
        custody.destroy(r.rid)                          # key destroyed at t_I (Ch4 s4.7 step 2)
    print(f"data keys destroyed (t_I finite)      : {len(invalidated)}")

    readable, refused = 0, 0
    for r in records:
        try:
            decrypt(custody, r.rid, *store[r.rid])
            readable += 1
        except KeyError:
            refused += 1
    print(f"decryptable after invalidation        : {readable}  (expected {len(records) - len(invalidated)})")
    print(f"refused, key destroyed                : {refused}  (expected {len(invalidated)})")

    # The ciphertext of an invalidated record does not open under any surviving key.
    victim = invalidated[0]
    survivors = [r for r in records if r.t_invalidation() == trf.INF]
    opened = 0
    for s in survivors:
        try:
            AESGCM(custody.data_key(s.rid)).decrypt(store[victim.rid][0], store[victim.rid][1],
                                                    f"rec:{victim.rid}".encode())
            opened += 1
        except InvalidTag:
            pass
    print(f"rid={victim.rid} ciphertext tried under {len(survivors)} surviving keys : opened {opened}")

    for r in invalidated:                               # then the ciphertext is deleted (D-17)
        del store[r.rid]
    print(f"ciphertexts kept after deletion       : {len(store)}")

    ok = (ok_before == len(records) and refused == len(invalidated)
          and readable == len(records) - len(invalidated) and opened == 0)
    print("=" * 74)
    print(f"RESULT: {'every invalidated record is unrecoverable; every other record reads' if ok else 'MISMATCH'}")
    print("=" * 74)


if __name__ == "__main__":
    main()
